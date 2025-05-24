import requests
import re
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
from io import BytesIO

def clean_description(text):
    return re.sub(r'<.*?>', '', text)

def get_champion_info():
    input_name = entry.get().lower()
    if input_name not in lowercase_map:
        output_box.config(state='normal')
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "Invalid champion name.")
        output_box.config(state='disabled')
        return

    champ_name = lowercase_map[input_name]
    url = f"https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion/{champ_name}.json"

    try:
        res = requests.get(url)
        data = res.json()
        champ = data['data'][champ_name]

        output = f"Name: {champ['name']}\n"
        output += f"Title: {champ['title']}\n"
        output += f"Role Tags: {', '.join(champ['tags'])}\n"
        output += f"Base HP: {champ['stats']['hp']}\n"
        output += f"Attack Damage: {champ['stats']['attackdamage']}\n\n"

        output += f"Passive: {champ['passive']['name']} - {clean_description(champ['passive']['description'])}\n\n"
        for i, spell in enumerate(champ['spells']):
            key = 'QWER'[i]
            name = spell['name']
            desc = clean_description(spell['description'])
            output += f"{key}: {name} - {desc}\n\n"

        output_box.config(state='normal')
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, output)
        output_box.config(state='disabled')

        # Load and display champion image
        img_url = f"https://ddragon.leagueoflegends.com/cdn/14.9.1/img/champion/{champ_name}.png"

        response = requests.get(img_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label.config(image=photo)
        img_label.image = photo # Keep ref to prevent GC

    except Exception as e:
        output_box.config(state='normal')
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"Error fetching data: {e}")
        output_box.config(state='disabled')

# Load champ list
CHAMP_LIST_URL = "https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion.json"
champ_list_response = requests.get(CHAMP_LIST_URL)
champ_data = champ_list_response.json()
champ_names = list(champ_data['data'].keys())
lowercase_map = {name.lower(): name for name in champ_names}

# Create GUI
root = tk.Tk()
root.title("LoL Champion Info")
root.configure(bg="#1e1e1e")  # Dark background

main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(padx=10, pady=10)

# Image display frame
img_frame = tk.Frame(main_frame, bg="#1e1e1e")
img_frame.pack(side=tk.LEFT, padx=10)

# Create a top frame specifically for the image (centered at top)
top_frame = tk.Frame(main_frame, bg="#1e1e1e")
top_frame.pack(fill=tk.X, pady=(0, 10))

# Placeholder image
default_img = Image.new('RGB', (120, 120), color='#1e1e1e')
default_photo = ImageTk.PhotoImage(default_img)
img_label = tk.Label(top_frame, image=default_photo, bg="#1e1e1e")
img_label.pack()

label = tk.Label(main_frame, text="Enter Champion Name:", fg="white", bg="#1e1e1e", font=("Segoe UI", 12, "bold"))
label.pack()

entry = tk.Entry(main_frame, width=30, bg="#2e2e2e", fg="white", insertbackground="white", font=("Segoe UI", 11))
entry.pack(pady=5)

btn = tk.Button(main_frame, text="Get Info", command=get_champion_info, bg="#3e3e3e", fg="white", font=("Segoe UI", 11))
btn.pack(pady=5)

output_box = scrolledtext.ScrolledText(
    main_frame, width=80, height=25, wrap=tk.WORD,
    bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 10)
)
output_box.pack(pady=10)
output_box.config(state='disabled')

root.mainloop()

