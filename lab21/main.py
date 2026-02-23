import flet as ft
import json
import sys
from pathlib import Path


APP_TITLE = "TaskBoard"
SAVE_FILE_NAME = "tasks.json"


def get_save_file_path() -> Path:
	if getattr(sys, "frozen", False):
		return Path(sys.executable).resolve().parent / SAVE_FILE_NAME
	return Path(__file__).resolve().parent / SAVE_FILE_NAME


class TaskItem(ft.Container):
	def __init__(self, title: str, on_toggle, on_delete):
		super().__init__()
		self.title = title
		self.on_toggle = on_toggle
		self.on_delete = on_delete
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

		self.content = ft.Row(
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
			controls=[
				ft.Row(
					spacing=10,
					controls=[self.checkbox, self.title_text],
				),
				self.delete_btn,
			],
		)

		self.bgcolor = ft.Colors.with_opacity(0.14, ft.Colors.WHITE)
		self.border_radius = 14
		self.padding = ft.Padding.symmetric(horizontal=12, vertical=8)
		self.apply_style()

	def apply_style(self):
		self.title_text.style = ft.TextStyle(
			decoration=ft.TextDecoration.LINE_THROUGH if self.is_done else None,
			color=ft.Colors.GREY_300 if self.is_done else ft.Colors.WHITE,
		)

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


def main(page: ft.Page):
	page.title = APP_TITLE
	page.padding = 0
	page.window_width = 920
	page.window_height = 620
	page.theme_mode = ft.ThemeMode.DARK
	page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

	tasks: list[TaskItem] = []

	total_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
	done_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

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
	save_file = get_save_file_path()
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

	def save_tasks():
		payload = [{"title": task.title, "done": task.is_done} for task in tasks]
		save_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

	def refresh_stats(save: bool = True):
		total = len(tasks)
		done = sum(1 for task in tasks if task.is_done)
		total_text.value = str(total)
		done_text.value = str(done)

		if total == 0:
			task_list.controls = [empty_state]
		else:
			task_list.controls = tasks

		if save:
			save_tasks()

		page.update()

	def load_tasks():
		if not save_file.exists():
			return
		try:
			stored_tasks = json.loads(save_file.read_text(encoding="utf-8"))
		except (json.JSONDecodeError, OSError):
			return

		if not isinstance(stored_tasks, list):
			return

		for row in stored_tasks:
			if not isinstance(row, dict):
				continue
			title = str(row.get("title", "")).strip()
			if not title:
				continue
			item = TaskItem(title, on_toggle=refresh_stats, on_delete=delete_task)
			item.set_done(bool(row.get("done", False)))
			tasks.append(item)

	def add_task():
		title = task_input.value.strip()
		if not title:
			task_input.error_text = "Please enter a task"
			page.update()
			return

		task_input.error_text = None
		item = TaskItem(title, on_toggle=refresh_stats, on_delete=delete_task)
		tasks.append(item)
		task_input.value = ""
		task_input.focus()
		refresh_stats()

	def delete_task(item: TaskItem):
		tasks.remove(item)
		refresh_stats()

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

	def clear_completed():
		nonlocal tasks
		tasks = [task for task in tasks if not task.is_done]
		refresh_stats()

	board = ft.Container(
		expand=True,
		padding=28,
		gradient=ft.LinearGradient(
			begin=ft.Alignment(-1, -1),
			end=ft.Alignment(1, 1),
			colors=["#1F1C2C", "#403B4A", "#2E335A"],
		),
		content=ft.Column(
			expand=True,
			spacing=18,
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
						clear_done_btn,
					],
				),
				ft.Row(
					spacing=12,
					controls=[task_input, add_btn],
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

	page.add(board)
	load_tasks()
	refresh_stats(save=False)


if __name__ == "__main__":
	ft.run(main)