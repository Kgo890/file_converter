import tkinter as tk
from tkinter import filedialog
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# define a class
class FileConverter:
    def __init__(self, root):
        # initialize the root window
        self.root = root
        self.root.title("File Converter")

        # Creating buttons to open file and exit button
        self.browse_button = tk.Button(root, text="Open File", command=self.browse_file)
        self.browse_button.pack()

        self.browse_button = tk.Button(root, text="Exit", command=root.destroy)
        self.browse_button.pack()

        # Creating Menus
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        convert_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Convert", menu=convert_menu)

        # Keep references to the menu items
        self.to_png_menu_item = tk.BooleanVar()
        self.to_jpeg_menu_item = tk.BooleanVar()
        self.to_pdf_menu_item = tk.BooleanVar()

        # adding checkbutton to show if the conversion be done
        convert_menu.add_checkbutton(label="To PNG", variable=self.to_png_menu_item, command=self.convert_to_png)
        convert_menu.add_checkbutton(label="To JPEG", variable=self.to_jpeg_menu_item, command=self.convert_to_jpeg)
        convert_menu.add_checkbutton(label="To PDF", variable=self.to_pdf_menu_item, command=self.convert_to_pdf)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_path = file_path

            # Enable the conversion options
            self.to_png_menu_item.set(True)
            self.to_jpeg_menu_item.set(True)
            self.to_pdf_menu_item.set(True)

    def convert_to_pdf(self):
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            if pdf_path == self.input_file_path:
                print("The file you want to convert has the same path")
                # disable the PDF conversion option (if you want to convert the same file type)
                self.to_pdf_menu_item.set(False)
            else:
                try:
                    # opens the image file and saves as a PDF
                    with Image.open(self.input_file_path) as img:
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_canvas = canvas.Canvas(pdf_file, pagesize=letter)
                            pdf_canvas.setPageSize((img.width, img.height))
                            pdf_canvas.drawInlineImage(img, 0, 0, width=img.width, height=img.height)
                            pdf_canvas.save()

                    print(f"Converting to PDF. Output path: {pdf_path}")
                except Exception as e:
                    print(f"Error: {e}")

    def convert_to_png(self):
        png_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        self.convert_file(png_path, 'PNG')

    def convert_to_jpeg(self):
        jpeg_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg")])
        self.convert_file(jpeg_path, "JPEG")

    def convert_file(self, output_path, format):
        if output_path:
            if output_path == self.input_file_path:
                # if the file you want to convert is the same (PNG and JPEG)
                print(f"The file you want to convert to {format} has the same path")
                if format == 'PNG':
                    self.to_png_menu_item.set(False)
                elif format == 'JPEG':
                    self.to_jpeg_menu_item.set(False)
            else:
                try:
                    print(f"Converting to {format}. Output path: {output_path}")
                except Exception as e:
                    print(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    converter = FileConverter(root)
    root.mainloop()
