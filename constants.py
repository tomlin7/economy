"""
constants are stored here.
"""
import json

import randomword as random_word

rank_emotes = ['🥇', '🥈', '🥉', '🔹', '🔹']

emoji_server_id = 790909556313686106
coin_emoji_id = 790909817790136330
coin_emoji = None

with open("names.json", "r") as people_list:
    people_file_data = json.load(people_list)
    people = people_file_data['names']
with open("beg_results.json", "r") as beg_results_file:
    beg_results_data = json.load(beg_results_file)
    beg_results = beg_results_data['results']
chances = [True, False]

salaries = {
    1: "upto 2000 coins per hour",
    2: "upto 1700 coins per hour",
    3: "upto 1400 coins per hour",
    4: "upto 1100 coins per hour",
    5: "upto 800 coins per hour",
    6: "upto 600 coins per hour"
}

jobs = {
    "Software Engineer": "Develop massive, complex software systems that scale globally.",
    "Product Manager": "manage a product's strategic planning to development and launch.",
    "Data Scientist": "Analyze data to build solutions and make recommendations.",
    "Electrical Engineer": "Maintain complex electrical control systems and equipment.",
    "Network Engineer": "Design network systems for Basement's operations",
    "Systems Integrator": "Integrate systems :)"
}


class Url:
    """
    URLs are stored in this class.
    """
    waldo_url = "https://media.discordapp.net/attachments/438385899873763328/786660791302094908/wheres_waldo.png"
