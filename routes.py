from flask import render_template, request, redirect, url_for, send_file
import os
from main import app
from pandas import read_csv
from datetime import datetime
from pycountry import countries


def clear_directory():
    # Clearing the files directory

    directory_path = app.config["UPLOAD_FOLDER"]
    for file in os.listdir(directory_path):
        print(file)
        os.remove(os.path.join(directory_path, file))


def change_csv(file_path, filename):
    data = read_csv(file_path, names=["ID", "Release Date", "Name", "Country", "Copies Sold", "Copy Price", "Total Revenue"])
    data.sort_values(["Release Date"], axis=0, ascending=[False], inplace=True)
    data = data[::-1]
    clear_directory()

    for i, row in data.iterrows():
        for el in range(len(row)):
            if el == 1:
                data.loc[i, "Release Date"] = datetime.strptime(row[el], "%Y/%m/%d").strftime("%d.%m.%Y")
            elif el == 2:
                data.loc[i, "Name"] = row[el].replace("-", " ").title()
            elif el == 3:
                data.loc[i, "Country"] = countries.get(alpha_3=row[el]).name
            elif el == 6:
                copy_price = float(row[5].replace(" USD", ""))
                total_revenue = str(round(copy_price * int(row[4]))).replace(".0", "")
                data.loc[i, "Total Revenue"] = f"{total_revenue} USD"

    # Deleting initial file and saving a new one
    os.remove(file_path)
    filename = filename.replace(".csv", "")
    upload_path = f"./{app.config['UPLOAD_FOLDER']}/{filename}_changed.csv"
    data.to_csv(upload_path)

    return upload_path


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Uploading file implementationgit commit -m "first commit"

    # Incorrect copy price line 2 (ID 4) and total revenue rounding to the nearest line 4 (ID 3)

    file = request.files["file"]
    if file.filename != "" and os.path.splitext(file.filename)[1] == ".csv":
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        upload_path = change_csv(path, file.filename)
        return send_file(upload_path, as_attachment=True)

    return redirect(url_for("main"))
