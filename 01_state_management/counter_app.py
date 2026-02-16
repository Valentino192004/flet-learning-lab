import flet as ft

def main(page: ft.Page):
    page.title = "Counter Pro | Flet"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    count = 0
    step = 1
    min_value = -999
    max_value = 999

    title = ft.Text("Counter Pro", size=22, weight=ft.FontWeight.W_600)
    subtitle = ft.Text("Flet + State + Events + UI composition", size=12, opacity=0.7)

    counter_field = ft.TextField(
        value=str(count),
        text_align=ft.TextAlign.CENTER,
        width=140,
        read_only=True,
        dense=True,
    )

    stats = ft.Text("", size=12, opacity=0.8)

    step_field = ft.TextField(
        value=str(step),
        label="Step",
        width=140,
        text_align=ft.TextAlign.CENTER,
        input_filter=ft.InputFilter(r"[0-9]"),
    )

    def clamp(n: int) -> int:
        return max(min_value, min(max_value, n))

    def refresh():
        nonlocal count, step
        counter_field.value = str(count)
        stats.value = f"Range: [{min_value}, {max_value}] | Current step: {step}"
        page.update()

    def read_step() -> int:
        value = (step_field.value or "").strip()
        try:
            s = int(value)
            return max(1, min(100, s))
        except ValueError:
            return 1

    def on_minus(e):
        nonlocal count, step
        step = read_step()
        count = clamp(count - step)
        refresh()

    def on_plus(e):
        nonlocal count, step
        step = read_step()
        count = clamp(count + step)
        refresh()

    def on_reset(e):
        nonlocal count
        count = 0
        refresh()

    def on_copy(e):
        page.set_clipboard(counter_field.value)
        page.snack_bar = ft.SnackBar(ft.Text("Copied to clipboard"))
        page.snack_bar.open = True
        page.update()

    btn_minus = ft.IconButton(
        icon=ft.Icons.REMOVE,
        tooltip="Decrease",
        on_click=on_minus,
    )
    btn_plus = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Increase",
        on_click=on_plus,
    )
    btn_reset = ft.ElevatedButton(
        "Reset",
        icon=ft.Icons.REFRESH,
        on_click=on_reset,
    )
    btn_copy = ft.OutlinedButton(
        "Copy",
        icon=ft.Icons.CONTENT_COPY,
        on_click=on_copy,
    )

    counter_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[btn_minus, counter_field, btn_plus],
    )

    actions_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[btn_reset, btn_copy],
    )

    step_row = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[step_field],
    )

    card = ft.Card(
        content=ft.Container(
            padding=20,
            width=420,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    title,
                    subtitle,
                    ft.Divider(height=1),
                    counter_row,
                    step_row,
                    actions_row,
                    stats,
                ],
            ),
        )
    )

    page.add(card)
    refresh()


ft.run(main)
