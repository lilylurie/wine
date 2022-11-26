import requests
import pandas as pd





country_code = {"ar": "Argentina", "at": "Austria", "au":"Australia", "br":"Brazil", "cl": "Chile", "de":"Germany", "es":"Spain", "fr":"France", "gb":"United Kingdom", "ge":"Georgia", "gr":"Greece", "it":"Italy", "pt":"Portugal", "us": "USA" }
type_code = {"1":"Red", "2":"White", "3":"Sparkling", "4": "Rose", "7": "Dessert", "24":"Fortified"}
def get_wine_data(wine_id, year, page):
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = "https://www.vivino.com/api/wines/{id}/reviews?per_page=50&year={year}&page={page}" # <— increased the number of reviews to 9999

    data = requests.get(
    api_url.format(id=wine_id, year=year, page=page), headers=headers).json()

    return data


r = requests.get(
"https://www.vivino.com/api/explore/explore",
params={
#"country_code": "PT",
"country_codes[]": ["ar", "at", "au", "br", "cl", "de", "es", "fr", "gb", "ge", "gr", "it", "pt", "us"],
"currency_code": "EUR",
"grape_filter": "varietal",
"min_rating": "1",
"order_by": "price",
"order": "asc",
"page": 1,
"price_range_max": "500",
"price_range_min": "0",
"wine_type_ids[]": ["1", "2", "3", "4", "7", "24"]
},
headers={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
},
)

results = [
(
t["vintage"]["wine"]["winery"]["name"],
t["vintage"]["year"],
t["vintage"]["wine"]["id"],
f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
t["vintage"]["statistics"]["ratings_average"],
t["vintage"]["statistics"]["ratings_count"],
type_code[str(t["vintage"]["wine"]["type_id"])],
f'{t["vintage"]["wine"]["region"]["country"]["name"]} {t["vintage"]["wine"]["region"]["name"]}',
t["vintage"]["wine"]["region"]["country"]["code"],
f'{t["vintage"]["wine"]["region"]["country"]["most_used_grapes"][0]["name"]} {t["vintage"]["wine"]["region"]["country"]["most_used_grapes"][1]["name"]}'
)
for t in r.json()["explore_vintage"]["matches"]
]
dataframe = pd.DataFrame(
results,
columns=["Winery", "Year", "Wine ID", "Wine", "Rating", "num_review", "Wine type", "Wine region", "Country", "Grape"],
)

ratings = []
for _, row in dataframe.iterrows():
    page = 1
    while True:
        print(
        f'Getting info about wine {row["Wine ID"]}-{row["Year"]} Page {page}'
        )

        d = get_wine_data(row["Wine ID"], row["Year"], page)
        print(d)

        if not d["reviews"]:
            break

        for r in d["reviews"]:
            ratings.append(
            [
            row["Year"],
            row["Wine ID"],
            r["rating"],
            r["note"],
            r["created_at"],
            r["user"]["id"],
            r["user"]["statistics"]["followers_count"],
            r["user"]["statistics"]["followings_count"],
            r["user"]["statistics"]["ratings_count"],
            r["language"]
            ]
            )

        page += 1
        if page == 10: break

        break

ratings = pd.DataFrame(
ratings, columns=["Year", "Wine ID", "User's Grade", "Note", "CreatedAt", "user id", "followers", "following", "User Ratings", "language"]
)

df_out = dataframe.merge(ratings)
df_out.to_csv("wine.csv", index=False, sep=';')
