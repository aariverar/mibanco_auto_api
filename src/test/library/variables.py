import os

html_features_template=os.getcwd()+"\\src\\test\\resources\\template\\overview-features.html"
html_for_each_feature_template=os.getcwd()+"\\src\\test\\resources\\template\\report-feature.html"
report_folder_path = os.getcwd()+"\\src\\test\\reports"
template_folder_path = os.getcwd()+"\\src\\test\\resources\\template"
source_files = ["logo_mibanco.png", "main.js", "style.css", "icon.ico"]

excel_path = os.getcwd()+"\\src\\test\\resources\\data\\excel\\test_data.xlsx" #TO DO
expected_columns = ["Expected Status Code",	"Expected Content_1", "Expected Content_2",
                        "Expected Content_3", "Expected Content_4",	"Expected Content_5", "Expected Content_6"]