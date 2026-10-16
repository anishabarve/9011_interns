def calculateMedicineTotal(price, quantity):
    return price * quantity


def calculateGST(amount):
    return amount * 0.05


def calculateDiscount(amount):
    return amount * 0.10


def calculateFinalBill(total, gst, discount):
    return total + gst - discount


def generateInvoice():
    # medicine details
    medicine1 = "Paracetamol"
    price1 = 50.00
    quantity1 = 2

    medicine2 = "Vitamin C"
    price2 = 100.00
    quantity2 = 1

    medicine3 = "Cough Syrup"
    price3 = 120.00
    quantity3 = 1

    # Calculate medicine totals
    total1 = calculateMedicineTotal(price1, quantity1)
    total2 = calculateMedicineTotal(price2, quantity2)
    total3 = calculateMedicineTotal(price3, quantity3)

    subtotal = total1 + total2 + total3
    gst = calculateGST(subtotal)
    discount = calculateDiscount(subtotal)
    finalAmount = calculateFinalBill(subtotal, gst, discount)

    # Print invoice
    print("========== MEDICAL INVOICE ==========")
    print(f"{'Medicine':<20}{'Price':>8}{'Qty':>6}{'Total':>10}")
    print("-" * 44)

    print(f"{medicine1:<20}{price1:>8.2f}{quantity1:>6}{total1:>10.2f}")
    print(f"{medicine2:<20}{price2:>8.2f}{quantity2:>6}{total2:>10.2f}")
    print(f"{medicine3:<20}{price3:>8.2f}{quantity3:>6}{total3:>10.2f}")

    print("-" * 44)
    print(f"Subtotal          = {subtotal:.2f}")
    print(f"GST (5%)          = {gst:.2f}")
    print(f"Discount (10%)    = {discount:.2f}")
    print(f"Final Bill Amount = {finalAmount:.2f}")
    print("=====================================")


generateInvoice()