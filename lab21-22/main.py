import asyncio
import ctypes
import datetime as dt
import inspect
import json
import sys
from pathlib import Path

import flet as ft

try:
	import winsound
except ImportError:
	winsound = None


APP_TITLE = "TaskBoard"
SAVE_FILE_NAME = "tasks.json"


def get_save_file_path() -> Path:
	if getattr(sys, "frozen", False):
		return Path(sys.executable).resolve().parent / SAVE_FILE_NAME
	return Path(__file__).resolve().parent / SAVE_FILE_NAME


class TaskItem(ft.Container):
	def __init__(self, title: str, on_toggle, on_delete, due_at: dt.datetime | None = None):
		super().__init__()
		self.title = title
		self.on_toggle = on_toggle
		self.on_delete = on_delete
		self.due_at = due_at
		self.reminded = False
		self.is_done = False

		self.checkbox = ft.Checkbox(value=False, on_change=self.handle_toggle)
		self.title_text = ft.Text(
			title,
			size=15,
			weight=ft.FontWeight.W_500,
			color=ft.Colors.WHITE,
			selectable=False,
		)
		self.delete_btn = ft.IconButton(
			icon=ft.Icons.DELETE_OUTLINE,
			icon_color=ft.Colors.RED_300,
			tooltip="Delete task",
			on_click=self.handle_delete,
		)
		self.due_text = ft.Text(size=12, color=ft.Colors.BLUE_GREY_100)

		self.content = ft.Row(
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Row(
					expand=True,
					spacing=10,
					controls=[
						self.checkbox,
						ft.Column(
							spacing=2,
							tight=True,
							expand=True,
							controls=[self.title_text, self.due_text],
						),
					],
				),
				self.delete_btn,
			],
		)

		self.bgcolor = ft.Colors.with_opacity(0.14, ft.Colors.WHITE)
		self.border_radius = 14
		self.padding = ft.Padding.symmetric(horizontal=12, vertical=8)
		self.update_due_text()
		self.apply_style()

	@staticmethod
	def format_due(due_at: dt.datetime | None) -> str:
		if due_at is None:
			return "Без дедлайну"
		return due_at.strftime("%d.%m.%Y %H:%M")

	def update_due_text(self, reminder_minutes: int = 20) -> bool:
		old_value = self.due_text.value
		old_color = self.due_text.color

		if self.due_at is None:
			new_value = "Без дедлайну"
			new_color = ft.Colors.BLUE_GREY_200
		elif self.is_done:
			new_value = f"Виконано • {self.format_due(self.due_at)}"
			new_color = ft.Colors.GREEN_300
		else:
			now = dt.datetime.now()
			seconds_left = int((self.due_at - now).total_seconds())
			if seconds_left < 0:
				new_value = f"Прострочено • {self.format_due(self.due_at)}"
				new_color = ft.Colors.RED_300
			elif seconds_left <= reminder_minutes * 60:
				minutes_left = max(1, seconds_left // 60)
				new_value = f"Скоро дедлайн • ~{minutes_left} хв"
				new_color = ft.Colors.AMBER_300
			else:
				new_value = f"До: {self.format_due(self.due_at)}"
				new_color = ft.Colors.BLUE_GREY_100

		if self.reminded and not self.is_done:
			new_value = f"{new_value}"

		self.due_text.value = new_value
		self.due_text.color = new_color
		return old_value != new_value or old_color != new_color

	def apply_style(self):
		self.title_text.style = ft.TextStyle(
			decoration=ft.TextDecoration.LINE_THROUGH if self.is_done else None,
			color=ft.Colors.GREY_300 if self.is_done else ft.Colors.WHITE,
		)
		self.update_due_text()

	def set_due(self, due_at: dt.datetime | None):
		self.due_at = due_at
		self.update_due_text()

	def set_done(self, value: bool):
		self.is_done = value
		self.checkbox.value = value
		self.apply_style()

	def handle_toggle(self, e: ft.ControlEvent):
		self.is_done = self.checkbox.value
		self.apply_style()
		self.update()
		self.on_toggle()

	def handle_delete(self, e: ft.ControlEvent):
		self.on_delete(self)

	def as_dict(self) -> dict:
		return {
			"title": self.title,
			"done": self.is_done,
			"due_at": self.due_at.isoformat() if self.due_at else None,
			"reminded": self.reminded,
		}


def main(page: ft.Page):
	page.title = APP_TITLE
	page.padding = 0
	page.window_width = 920
	page.window_height = 620
	page.theme_mode = ft.ThemeMode.DARK
	page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

	tasks: list[TaskItem] = []
	save_file = get_save_file_path()

	def read_storage() -> tuple[list[dict], dict]:
		if not save_file.exists():
			return [], {}
		try:
			stored = json.loads(save_file.read_text(encoding="utf-8"))
		except (json.JSONDecodeError, OSError):
			return [], {}

		if isinstance(stored, list):
			return stored, {}
		if isinstance(stored, dict):
			tasks_data = stored.get("tasks", [])
			settings_data = stored.get("settings", {})
			if isinstance(tasks_data, list) and isinstance(settings_data, dict):
				return tasks_data, settings_data
		return [], {}

	stored_tasks_data, stored_settings = read_storage()

	background_image_path = stored_settings.get("background_image")
	if not isinstance(background_image_path, str) or not background_image_path.strip():
		background_image_path = None
	elif not Path(background_image_path).exists():
		background_image_path = None

	raw_image_history = stored_settings.get("image_history", [])
	image_history: list[str] = []
	if isinstance(raw_image_history, list):
		seen_images: set[str] = set()
		for entry in raw_image_history:
			if not isinstance(entry, str):
				continue
			normalized = entry.strip()
			if not normalized:
				continue
			if normalized in seen_images:
				continue
			seen_images.add(normalized)
			image_history.append(normalized)

	if background_image_path and background_image_path not in image_history:
		image_history.insert(0, background_image_path)

	try:
		background_opacity = float(stored_settings.get("background_opacity", 0.35))
	except (TypeError, ValueError):
		background_opacity = 0.35
	background_opacity = min(0.9, max(0.0, background_opacity))

	custom_ringtone_path = stored_settings.get("custom_ringtone")
	if not isinstance(custom_ringtone_path, str) or not custom_ringtone_path.strip():
		custom_ringtone_path = None
	elif not Path(custom_ringtone_path).exists():
		custom_ringtone_path = None

	raw_ringtone_history = stored_settings.get("ringtone_history", [])
	ringtone_history: list[str] = []
	if isinstance(raw_ringtone_history, list):
		seen_paths: set[str] = set()
		for entry in raw_ringtone_history:
			if not isinstance(entry, str):
				continue
			normalized = entry.strip()
			if not normalized:
				continue
			if normalized in seen_paths:
				continue
			seen_paths.add(normalized)
			ringtone_history.append(normalized)

	if custom_ringtone_path and custom_ringtone_path not in ringtone_history:
		ringtone_history.insert(0, custom_ringtone_path)

	use_custom_ringtone = bool(stored_settings.get("use_custom_ringtone", False))

	try:
		reminder_minutes = int(stored_settings.get("reminder_minutes", 20))
	except (TypeError, ValueError):
		reminder_minutes = 20
	reminder_minutes = max(0, min(240, reminder_minutes))

	selected_due_date: dt.date | None = None
	selected_due_time: dt.time | None = None
	selected_due_at: dt.datetime | None = None

	total_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
	done_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
	selected_due_text = ft.Text("Термін: не вибрано", size=12, color=ft.Colors.BLUE_GREY_100)
	background_status_text = ft.Text(size=12, color=ft.Colors.BLUE_GREY_100)
	ringtone_status_text = ft.Text(size=12, color=ft.Colors.BLUE_GREY_100)
	reminder_minutes_text = ft.Text(size=12, color=ft.Colors.BLUE_GREY_100)

	background_layer = ft.Container(
		expand=True,
		gradient=ft.LinearGradient(
			begin=ft.Alignment(-1, -1),
			end=ft.Alignment(1, 1),
			colors=["#1F1C2C", "#403B4A", "#2E335A"],
		),
	)
	image_layer = ft.Container(expand=True, visible=False)
	image_overlay_layer = ft.Container(expand=True, visible=False)

	task_input = ft.TextField(
		hint_text="Які твої плани на сьогодні?",
		border_radius=12,
		expand=True,
		bgcolor=ft.Colors.with_opacity(0.09, ft.Colors.WHITE),
		border_color=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
		text_style=ft.TextStyle(color=ft.Colors.WHITE),
		hint_style=ft.TextStyle(color=ft.Colors.BLUE_GREY_200),
		autofocus=True,
		on_submit=lambda e: add_task(),
	)

	task_list = ft.ListView(expand=True, spacing=8, auto_scroll=False)
	mp3_alias = "taskboard_mp3"
	empty_state = ft.Container(
		padding=20,
		border_radius=14,
		bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
		content=ft.Text(
			"Поки нема завдань, добавляй)",
			size=15,
			color=ft.Colors.BLUE_GREY_100,
			text_align=ft.TextAlign.CENTER,
		),
	)

	def show_notice(text: str):
		page.snack_bar = ft.SnackBar(content=ft.Text(text), open=True)
		page.update()

	def play_ringtone():
		ctypes.windll.winmm.mciSendStringW(f"close {mp3_alias}", None, 0, None)

		if use_custom_ringtone and custom_ringtone_path and Path(custom_ringtone_path).exists():
			ext = Path(custom_ringtone_path).suffix.lower()
			if ext == ".wav" and winsound is not None:
				winsound.PlaySound(custom_ringtone_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
				return

			if ext == ".mp3":
				path_escaped = custom_ringtone_path.replace('"', '""')
				open_result = ctypes.windll.winmm.mciSendStringW(
					f'open "{path_escaped}" type mpegvideo alias {mp3_alias}',
					None,
					0,
					None,
				)
				if open_result == 0:
					ctypes.windll.winmm.mciSendStringW(f"play {mp3_alias}", None, 0, None)
					return

			show_notice("Не вдалося відтворити кастомний рінгтон")
			return

		if winsound is not None:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

	def stop_ringtone(e: ft.ControlEvent | None = None):
		if winsound is not None:
			winsound.PlaySound(None, 0)
		ctypes.windll.winmm.mciSendStringW(f"stop {mp3_alias}", None, 0, None)
		ctypes.windll.winmm.mciSendStringW(f"close {mp3_alias}", None, 0, None)

	def task_from_row(row: dict) -> TaskItem | None:
		if not isinstance(row, dict):
			return None

		title = str(row.get("title", "")).strip()
		if not title:
			return None

		due_at = None
		due_raw = row.get("due_at")
		if isinstance(due_raw, str) and due_raw.strip():
			try:
				due_at = dt.datetime.fromisoformat(due_raw)
			except ValueError:
				due_at = None

		item = TaskItem(title=title, on_toggle=refresh_stats, on_delete=delete_task, due_at=due_at)
		item.reminded = bool(row.get("reminded", False))
		item.set_done(bool(row.get("done", False)))
		item.update_due_text()
		return item

	def save_tasks():
		payload = {
			"tasks": [task.as_dict() for task in tasks],
			"settings": {
				"background_image": background_image_path,
				"image_history": image_history,
				"background_opacity": background_opacity,
				"custom_ringtone": custom_ringtone_path,
				"ringtone_history": ringtone_history,
				"use_custom_ringtone": use_custom_ringtone,
				"reminder_minutes": reminder_minutes,
			},
		}
		save_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

	def update_background_ui():
		image_exists = bool(background_image_path)
		image_layer.visible = image_exists
		image_layer.image = (
			ft.DecorationImage(src=background_image_path, fit=ft.BoxFit.COVER) if image_exists else None
		)

		image_overlay_layer.visible = image_exists
		image_overlay_layer.bgcolor = ft.Colors.with_opacity(background_opacity, ft.Colors.BLACK)

		opacity_slider.disabled = not image_exists
		opacity_slider.value = background_opacity
		background_history_dropdown.options = [
			ft.dropdown.Option(key=path, text=Path(path).name) for path in image_history
		]
		background_history_dropdown.value = background_image_path if background_image_path in image_history else None
		background_status_text.value = (
			f"Фон: {Path(background_image_path).name}" if image_exists else "Фон: градієнт"
		)

	def add_background_to_history(path: str):
		normalized = path.strip()
		if not normalized:
			return
		if normalized in image_history:
			image_history.remove(normalized)
		image_history.insert(0, normalized)
		if len(image_history) > 30:
			del image_history[30:]

	def update_ringtone_ui():
		ringtone_picker_btn.disabled = not use_custom_ringtone
		ringtone_history_dropdown.disabled = not use_custom_ringtone
		ringtone_history_dropdown.options = [
			ft.dropdown.Option(key=path, text=Path(path).name) for path in ringtone_history
		]
		ringtone_history_dropdown.value = custom_ringtone_path if custom_ringtone_path in ringtone_history else None
		if use_custom_ringtone and custom_ringtone_path:
			ringtone_status_text.value = f"Рінгтон: {Path(custom_ringtone_path).name}"
		elif use_custom_ringtone:
			ringtone_status_text.value = "Рінгтон: вибери файл"
		else:
			ringtone_status_text.value = "Рінгтон: системний (default)"

	def add_ringtone_to_history(path: str):
		normalized = path.strip()
		if not normalized:
			return
		if normalized in ringtone_history:
			ringtone_history.remove(normalized)
		ringtone_history.insert(0, normalized)
		if len(ringtone_history) > 30:
			del ringtone_history[30:]

	def update_reminder_ui():
		reminder_slider.value = reminder_minutes
		reminder_minutes_text.value = f"Нагадування за: {reminder_minutes} хв до дедлайну"

	def reset_due_picker():
		nonlocal selected_due_date, selected_due_time, selected_due_at
		selected_due_date = None
		selected_due_time = None
		selected_due_at = None
		selected_due_text.value = "Термін: не вибрано"

	def update_selected_due():
		nonlocal selected_due_at
		if selected_due_date and selected_due_time:
			selected_due_at = dt.datetime.combine(selected_due_date, selected_due_time)
			selected_due_text.value = f"Термін: {selected_due_at.strftime('%d.%m.%Y %H:%M')}"
		elif selected_due_date:
			selected_due_at = None
			selected_due_text.value = f"Дата: {selected_due_date.strftime('%d.%m.%Y')} (обери час)"
		elif selected_due_time:
			selected_due_at = None
			selected_due_text.value = "Час обрано (обери дату)"
		else:
			selected_due_at = None
			selected_due_text.value = "Термін: не вибрано"

	def refresh_stats(save: bool = True):
		total = len(tasks)
		done = sum(1 for task in tasks if task.is_done)
		total_text.value = str(total)
		done_text.value = str(done)

		for task in tasks:
			task.update_due_text(reminder_minutes)

		if total == 0:
			task_list.controls = [empty_state]
		else:
			task_list.controls = tasks

		if save:
			save_tasks()

		page.update()

	def delete_task(item: TaskItem):
		tasks.remove(item)
		refresh_stats()

	def load_tasks():
		for row in stored_tasks_data:
			item = task_from_row(row)
			if item:
				tasks.append(item)

	def add_task():
		title = task_input.value.strip()
		if not title:
			task_input.error_text = "Введи задачу"
			page.update()
			return

		task_input.error_text = None
		item = TaskItem(title, on_toggle=refresh_stats, on_delete=delete_task, due_at=selected_due_at)
		tasks.append(item)
		task_input.value = ""
		task_input.focus()
		reset_due_picker()
		refresh_stats()

	def clear_completed():
		nonlocal tasks
		tasks = [task for task in tasks if not task.is_done]
		refresh_stats()

	def on_date_selected(e: ft.ControlEvent):
		nonlocal selected_due_date
		if date_picker.value:
			if isinstance(date_picker.value, dt.datetime):
				if date_picker.value.tzinfo is not None:
					selected_due_date = date_picker.value.astimezone().date()
				else:
					selected_due_date = date_picker.value.date()
			else:
				selected_due_date = date_picker.value
			update_selected_due()
			page.update()

	def on_time_selected(e: ft.ControlEvent):
		nonlocal selected_due_time
		if time_picker.value:
			selected_due_time = time_picker.value
			update_selected_due()
			page.update()

	def open_date_picker(e: ft.ControlEvent):
		date_picker.open = True
		page.update()

	def open_time_picker(e: ft.ControlEvent):
		time_picker.open = True
		page.update()

	def clear_due_selection(e: ft.ControlEvent):
		reset_due_picker()
		page.update()

	def on_background_selected(files):
		nonlocal background_image_path
		if files and len(files) > 0 and getattr(files[0], "path", None):
			selected_path = files[0].path
			if Path(selected_path).suffix.lower() == ".mp4":
				show_notice("MP4 фон не підтримується у цій версії застосунку. Використай png/jpg/webp/gif")
				return
			background_image_path = selected_path
			add_background_to_history(background_image_path)
			update_background_ui()
			save_tasks()
			page.update()

	def on_background_history_select(e: ft.ControlEvent):
		nonlocal background_image_path
		selected = background_history_dropdown.value
		if not selected:
			return
		if not Path(selected).exists():
			show_notice("Файл фону не знайдено")
			return
		background_image_path = selected
		add_background_to_history(background_image_path)
		update_background_ui()
		save_tasks()
		page.update()

	def remove_background(e: ft.ControlEvent):
		nonlocal background_image_path
		background_image_path = None
		update_background_ui()
		save_tasks()
		page.update()

	def on_opacity_change(e: ft.ControlEvent):
		nonlocal background_opacity
		background_opacity = float(opacity_slider.value)
		update_background_ui()
		save_tasks()
		page.update()

	def on_ringtone_mode_change(e: ft.ControlEvent):
		nonlocal use_custom_ringtone
		use_custom_ringtone = bool(custom_ringtone_switch.value)
		update_ringtone_ui()
		save_tasks()
		page.update()

	def on_ringtone_selected(files):
		nonlocal custom_ringtone_path
		if files and len(files) > 0 and getattr(files[0], "path", None):
			custom_ringtone_path = files[0].path
			add_ringtone_to_history(custom_ringtone_path)
			update_ringtone_ui()
			save_tasks()
			page.update()

	def on_ringtone_history_select(e: ft.ControlEvent):
		nonlocal custom_ringtone_path
		selected = ringtone_history_dropdown.value
		if not selected:
			return
		custom_ringtone_path = selected
		add_ringtone_to_history(custom_ringtone_path)
		update_ringtone_ui()
		save_tasks()
		page.update()

	def on_reminder_minutes_change(e: ft.ControlEvent):
		nonlocal reminder_minutes
		reminder_minutes = int(round(float(reminder_slider.value)))
		reminder_minutes = max(0, min(240, reminder_minutes))
		update_reminder_ui()
		refresh_stats(save=False)
		save_tasks()
		page.update()

	def test_ringtone(e: ft.ControlEvent):
		play_ringtone()

	async def pick_background_async():
		picked = background_picker.pick_files(
			dialog_title="Обери зображення для фону",
			file_type=ft.FilePickerFileType.CUSTOM,
			allowed_extensions=["png", "jpg", "jpeg", "webp", "bmp", "gif"],
		)
		if inspect.isawaitable(picked):
			picked = await picked
		on_background_selected(picked)

	async def pick_ringtone_async():
		picked = ringtone_picker.pick_files(
			dialog_title="Обери рінгтон",
			file_type=ft.FilePickerFileType.CUSTOM,
			allowed_extensions=["wav", "mp3"],
		)
		if inspect.isawaitable(picked):
			picked = await picked
		on_ringtone_selected(picked)

	def pick_background(e: ft.ControlEvent):
		page.run_task(pick_background_async)

	def pick_ringtone(e: ft.ControlEvent):
		page.run_task(pick_ringtone_async)

	async def reminder_loop():
		while True:
			was_changed = False
			now = dt.datetime.now()
			for task in tasks:
				label_changed = task.update_due_text(reminder_minutes)
				if label_changed:
					was_changed = True

				if task.is_done or task.due_at is None or task.reminded:
					continue

				reminder_time = task.due_at - dt.timedelta(minutes=reminder_minutes)
				if now >= reminder_time:
					task.reminded = True
					task.update_due_text(reminder_minutes)
					play_ringtone()
					show_notice(f"Нагадування: '{task.title}' завершується о {task.due_at.strftime('%H:%M')}")
					was_changed = True

			if was_changed:
				save_tasks()
				page.update()

			await asyncio.sleep(15)

	date_picker = ft.DatePicker(on_change=on_date_selected)
	time_picker = ft.TimePicker(on_change=on_time_selected)
	background_picker = ft.FilePicker()
	ringtone_picker = ft.FilePicker()
	page.overlay.extend([date_picker, time_picker])
	page.services.extend([background_picker, ringtone_picker])

	add_btn = ft.Button(
		"Додати",
		icon=ft.Icons.ADD,
		on_click=lambda e: add_task(),
		style=ft.ButtonStyle(
			bgcolor=ft.Colors.WHITE,
			color=ft.Colors.INDIGO_700,
			padding=ft.Padding.symmetric(horizontal=22, vertical=16),
			shape=ft.RoundedRectangleBorder(radius=12),
		),
	)

	clear_done_btn = ft.TextButton(
		"Очистити виконані",
		icon=ft.Icons.CLEANING_SERVICES,
		on_click=lambda e: clear_completed(),
		style=ft.ButtonStyle(color=ft.Colors.WHITE),
	)

	def open_settings(e: ft.ControlEvent):
		settings_dialog.open = True
		page.update()

	def close_settings(e: ft.ControlEvent):
		settings_dialog.open = False
		page.update()

	settings_btn = ft.IconButton(
		icon=ft.Icons.SETTINGS,
		icon_color=ft.Colors.WHITE,
		tooltip="Налаштування",
		on_click=open_settings,
	)

	quick_stop_btn = ft.IconButton(
		icon=ft.Icons.STOP,
		icon_color=ft.Colors.WHITE,
		icon_size=34,
		style=ft.ButtonStyle(
			bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
			shape=ft.CircleBorder(),
		),
		tooltip="Стоп",
		on_click=stop_ringtone,
	)

	opacity_slider = ft.Slider(
		min=0,
		max=0.9,
		divisions=9,
		value=background_opacity,
		expand=True,
		on_change=on_opacity_change,
	)

	custom_ringtone_switch = ft.Switch(
		label="Кастомний рінгтон",
		value=use_custom_ringtone,
		on_change=on_ringtone_mode_change,
	)

	reminder_slider = ft.Slider(
		min=0,
		max=240,
		divisions=48,
		value=reminder_minutes,
		on_change=on_reminder_minutes_change,
	)

	ringtone_picker_btn = ft.TextButton(
		"Обрати рінгтон",
		icon=ft.Icons.MUSIC_NOTE,
		on_click=pick_ringtone,
	)

	test_ringtone_btn = ft.TextButton(
		"Тест рінгтону",
		icon=ft.Icons.PLAY_ARROW,
		on_click=test_ringtone,
	)

	stop_ringtone_btn = ft.TextButton(
		"Стоп",
		icon=ft.Icons.STOP,
		on_click=stop_ringtone,
	)

	background_history_dropdown = ft.Dropdown(
		label="Попередні фони",
		hint_text="Вибери з раніше доданих",
		enable_search=True,
		on_select=on_background_history_select,
	)

	ringtone_history_dropdown = ft.Dropdown(
		label="Попередні рінгтони",
		hint_text="Вибери з раніше доданих",
		enable_search=True,
		on_select=on_ringtone_history_select,
	)

	settings_dialog = ft.AlertDialog(
		modal=True,
		title=ft.Text("Налаштування", color=ft.Colors.WHITE),
		bgcolor=ft.Colors.BLUE_GREY_900,
		content=ft.Container(
			width=560,
			content=ft.Column(
				tight=True,
				spacing=10,
				controls=[
					ft.Row(
						controls=[
							ft.TextButton("Поставити фон", icon=ft.Icons.IMAGE, on_click=pick_background),
							ft.TextButton("Забрати фон", icon=ft.Icons.DELETE, on_click=remove_background),
						],
					),
					background_history_dropdown,
					background_status_text,
					ft.Row(
						spacing=10,
						controls=[ft.Text("Opacity", color=ft.Colors.WHITE), opacity_slider],
					),
					custom_ringtone_switch,
					ft.Row(controls=[ringtone_picker_btn, test_ringtone_btn, stop_ringtone_btn]),
					ringtone_history_dropdown,
					ringtone_status_text,
					ft.Divider(color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
					reminder_minutes_text,
					reminder_slider,
				],
			),
		),
		actions=[ft.TextButton("Закрити", on_click=close_settings)],
		actions_alignment=ft.MainAxisAlignment.END,
	)
	page.overlay.append(settings_dialog)

	content = ft.Container(
		expand=True,
		padding=28,
		content=ft.Column(
			expand=True,
			spacing=14,
			controls=[
				ft.Row(
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
					controls=[
						ft.Column(
							spacing=2,
							controls=[
								ft.Text("Мої завдання", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
								ft.Text("Будь зосередженим і оставайся сильним", size=14, color=ft.Colors.BLUE_GREY_100),
							],
						),
						ft.Row(controls=[settings_btn, clear_done_btn]),
					],
				),
				ft.Row(
					spacing=12,
					controls=[task_input, add_btn],
				),
				ft.Row(
					spacing=8,
					controls=[
						ft.TextButton("Дата", icon=ft.Icons.CALENDAR_MONTH, on_click=open_date_picker),
						ft.TextButton("Час", icon=ft.Icons.ACCESS_TIME, on_click=open_time_picker),
						ft.TextButton("Скинути термін", icon=ft.Icons.CLOSE, on_click=clear_due_selection),
						selected_due_text,
					],
				),
				ft.Row(
					spacing=14,
					controls=[
						ft.Container(
							padding=16,
							border_radius=14,
							bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
							content=ft.Column(
								tight=True,
								controls=[
									ft.Text("Всього", size=12, color=ft.Colors.BLUE_GREY_100),
									total_text,
								],
							),
						),
						ft.Container(
							padding=16,
							border_radius=14,
							bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
							content=ft.Column(
								tight=True,
								controls=[
									ft.Text("Виконано", size=12, color=ft.Colors.BLUE_GREY_100),
									done_text,
								],
							),
						),
					],
				),
				ft.Container(expand=True, content=task_list),
			],
		),
	)

	board = ft.Stack(
		expand=True,
		controls=[
			background_layer,
			image_layer,
			image_overlay_layer,
			content,
			ft.Container(
				right=20,
				top=230,
				content=quick_stop_btn,
			),
		],
	)

	page.add(board)
	update_background_ui()
	update_ringtone_ui()
	update_reminder_ui()
	load_tasks()
	refresh_stats(save=False)
	page.run_task(reminder_loop)


if __name__ == "__main__":
	ft.run(main)