import os
import re

import numpy as np
import pyautogui
import pytesseract
from botcity.core import DesktopBot
from PIL import Image, ImageEnhance, ImageFilter

from config.const import TESSERACT_PATH


class InvoiceRecord(DesktopBot):
    def __init__(self, path_app: str):
        super().__init__()
        self.path_app = path_app

    def not_found(self, label: str) -> None:
        """Print the error message if the element is not found

        Args:
            label (str): Name of the label/element to found in the system application
        """
        print(f"\nElement not found: {label}")

    def open_app(self) -> bool:
        """Open the application

        Returns:
            bool: return true if openned application succeeded
        """

        print("\nOpening application...")
        self.execute(self.path_app)
        self.wait(4000)
        self.maximize_window()
        self.wait(1000)

        print("\nAccessing invoices menu...")
        invoice_menu_exists = self.find("invoices", matching=0.97, waiting_time=10000)

        if not invoice_menu_exists:
            self.not_found("invoices")
        self.click()

        return invoice_menu_exists

    def invoice_record(
        self, date: str, account: str, contact: str, amount: int, status: str
    ) -> str:
        """Record an invoice in desktop system contoso

        Args:
            date (str): date of invoice
            account (str): account name of invoice
            contact (str): email contact of invoice
            amount (int): amount to invoice
            status (str): status of invoice

        Returns:
            str: message of invoice recorded in desktop with record ID.
        """

        # Click on new record button
        if not self.find("new-record", matching=0.97, waiting_time=10000):
            self.not_found("new-record")
        self.click()

        # Type date
        if not self.find("date", matching=0.97, waiting_time=10000):
            self.not_found("date")
        self.click_relative(66, 7)
        self.type_keys(["ctrl", "a"])
        date = date.split(" ")
        self.paste(date[0].replace("-", "/"))

        # Type account
        if not self.find("account", matching=0.97, waiting_time=10000):
            self.not_found("account")
        self.click_relative(80, 6)
        self.paste(account)

        # Type contact
        if not self.find("contact", matching=0.97, waiting_time=10000):
            self.not_found("contact")
        self.click_relative(95, 8)
        self.paste(contact)

        # Type amount
        if not self.find("amount", matching=0.97, waiting_time=10000):
            self.not_found("amount")
        self.click_relative(91, 7)
        self.paste(amount)

        # Click on selection status button
        if not self.find("status-inicio", matching=0.97, waiting_time=10000):
            self.not_found("status-inicio")
        self.click_relative(78, 6)

        # Check record status for selected status in contoso app
        status.title()
        match status:
            case "Uninvoiced":
                if not self.find(
                    "status-uninvoiced", matching=0.97, waiting_time=10000
                ):
                    self.not_found("status-uninvoiced")
                self.click_relative(70, 29)
            case "Invoiced":
                if not self.find("status-invoiced", matching=0.97, waiting_time=10000):
                    self.not_found("status-invoiced")
                self.click_relative(75, 51)
            case "Paid":
                if not self.find("status-paid", matching=0.97, waiting_time=10000):
                    self.not_found("status-paid")
                self.click_relative(71, 68)
            case _:
                print("\nInvalid status")

        # Get Invoice ID
        invoice_id = self.read_invoice_id()

        # save record
        if not self.find("save", matching=0.97, waiting_time=10000):
            self.not_found("save")
        self.click()

        return f"invoice registered successfully, id: {invoice_id}"

    def read_invoice_id(self) -> str:
        """Get invoice id generate by system using ocr on the recorder screenshot.

        Returns:
            str: invoice id generated or error message Invoice ID not found if an error occurred.
        """

        def preprocess_image(image_path: str) -> np.ndarray:
            """Preprocess image for OCR.

            Args:
                image_path (str): path to the image file

            Returns:
                np.ndarray: preprocessed image for OCR
            """
            image = Image.open(image_path)

            # Change to gray scale
            image = image.convert("L")

            # Improve contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)

            # Apply filter to improve sharpness
            image = image.filter(ImageFilter.SHARPEN)

            # Adjust brightness
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.5)

            # Convert PIL image to a NumPy array
            image_np = np.array(image)

            return image_np

        def extract_text(image_np: np.ndarray) -> str:
            """Extract text from image using OCR.

            Args:
                image_np (np.ndarray): preprocessed image for OCR

            Returns:
                str: extracted text from the image
            """
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
            extract_text = pytesseract.image_to_string(f"screenshot.png")

            return extract_text

        screenshot = pyautogui.screenshot()
        current_dir = os.getcwd()
        temp_dir = (
            os.path.join(current_dir, "data", "temp")
            if "temp" not in current_dir
            else current_dir
        )

        os.chdir(temp_dir)

        screenshot.save("screenshot.png")
        num = preprocess_image("screenshot.png")

        extracted_text = extract_text(num)

        os.remove("screenshot.png")

        pattern = r"WD:\s*(\d+)"
        match = re.search(pattern, extracted_text)

        return match.group(1) if match else f"Invoice ID not found: {extracted_text}"

    def close_app(self) -> None:
        """Close the application"""
        print("\nClosing application...")
        self.alt_f4()
