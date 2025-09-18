from django.shortcuts import render


def main_page(request, page="Home"):
    sections = ["Home", "Frontend", "Backend", "Contact"]

    # Starlar uchun hisoblash
    stars = [
        {"top": -i * 20, "left": (i * 47) % 1000, "duration": 2 + i % 5}
        for i in range(70)
    ]

    return render(request, "main_page.html", {
        "sections": sections,
        "current_page": page,
        "stars": stars
    })
