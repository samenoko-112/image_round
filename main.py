from PIL import Image, ImageDraw, ImageOps
import flet as ft
import sys

def main(page:ft.Page):
    page.title = "画像丸メール"
    page.padding = 20

    def round_image(e):
        image = Image.open(input_file.value).convert("RGBA")
        width, height = image.size

        mask = Image.new('L', (width,height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, width, height), radius=int(round_value.value), fill=255)

        rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        rounded_image.putalpha(mask)

        new_image_path = input_file.value.rsplit(".", 1)[0] + "_rounded.png"
        rounded_image.save(new_image_path)
        result.src = new_image_path
        result.visible = True
        result.update()
        page.snack_bar = ft.SnackBar(ft.Text("Done!"))
        page.snack_bar.open = True
        page.update()

    def input_file_select(e: ft.FilePickerResultEvent):
        input_file.value = e.files[0].path
        input_file.update()

    input_file_picker = ft.FilePicker(on_result=input_file_select)
    page.overlay.append(input_file_picker)
    input_file = ft.TextField("",on_focus=lambda _: input_file_picker.pick_files(dialog_title="Select Image",allowed_extensions=["jpg","png","jpeg"]),label="ファイル")
    round_value = ft.TextField("30",hint_text="丸める量",label="丸める量")

    run_btn = ft.FloatingActionButton(icon=ft.icons.PLAY_ARROW,on_click=round_image)

    result = ft.Image(
        visible=False,
        width=500,
        height=500,
    )

    page.add(
        input_file,
        round_value,
        run_btn,
        result
    )

if __name__ == "__main__":
    ft.app(target=main)
