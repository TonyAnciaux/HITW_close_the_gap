import pandas as pd
import numpy as np


class DfFormating:
    """
    input: path of Excel file
    Class to standardize Excel files into a Dataframe
    output: csv file
    """

    def __init__(self, path, donor=None):

        self.final_df: pd.DataFrame = None
        self.path: str = path
        self.donor: str = donor
        self.excel_file = path.split("/")
        self.index: dict = {"Quantity": ["Qty", "Quantity"],
                            "Reference": ["Book No.", "PATNumber", "Reference"],
                            "Serial Number": ["Serial no.", "Serial number", "Serialnumber asset"],
                            "Asset Tag": ["Asset Tag", "Client Asset Tag"],
                            "Type": ["Product type", "Product", "Stock Type"],
                            "Brand": ["Brand", "Manufacturer"],
                            "Model": ["Model"],
                            "Processor": ["Processor"],
                            "RAM": ["Memory", "RAM"],
                            "HDD": ["Drive Size", "HDD"],
                            "Display": ["DISPLAY SIZES", "Screen size"],
                            "Weight": ["Weight (KG)", "Weight"],
                            "Grade": ["Grade", "Condition Code", "GRADE-IN"],
                            "Defects": ["Defects", "Stock Comments"],
                            "Disk Status": ["Disk Status", "Erasure Status"],
                            "Donor": ["Donor"]
                            }
        self.types = {
            "LT": "Laptop", "NOTEBOOK": "Laptop", "Notebook": "laptop", "Desktop": "Desktop",
            "DESKTOP": "Desktop", "PC": "Desktop", "CS": "Monitor", "MS": "Monitor", "LD": "Monitor",
            "FS": "Monitor", "FLAT PANEL / MONITOR": "Monitor", "Monitor": "Monitor"}

        if self.excel_file[-1][:2] == "LB":
            self.lb_parsing()
        elif self.excel_file[-1][:2] == "CT":
            self.ct_parsing()
        else:
            self.tes_parsing()

    def lb_parsing(self):
        """
        Parses excels files to pd DataFrame from CTG Circular folder style
        """
        df = pd.read_excel(self.path, header=[2])
        new = df["Specifications"].str.split(",", expand=True)[0][:2]
        df["Processor"] = str(new[0]) + "," + str(new[1])
        df["RAM"] = df["Specifications"].str.split(",", expand=True)[2]
        df["HDD"] = df["Specifications"].str.split(",", expand=True)[3]
        df["Reference"] = df["Load no."].astype(str) + " - " + df["Tracking reference"].astype(str)
        self.final_df = df
        self.create_df()

    def ct_parsing(self):
        """
        Parses excels files to pd DataFrame from PlanBit folder style
        """

        df = pd.read_excel(self.path)
        df["Defects"] = df["Defect 1"] + "," + df["Defect 2"] + "," + df["Defect 3"] + "," + df["Defect 4"] + "," + df[
            "Defect 5"]
        donor_name = self.path.split(" ")
        del (donor_name[:3], donor_name[-2:])
        df["Donor"] = " ".join(donor_name)
        self.final_df = df
        return self.create_df()

    def tes_parsing(self):
        """
        Parses excels files to pd DataFrame from TES folder style
        """

        df = pd.read_excel(self.path, header=[18])
        df["Donor"] = pd.read_excel(self.path, usecols="B", header=None, names=["Donor"]).iloc[2]["Donor"]
        self.final_df = df
        self.create_df()

    def create_df(self):
        """
        :input: pd.DataFrame
        Create standardized DataFrame
        :output: pd.DataFrame
        """

        df = self.final_df
        new_df = pd.DataFrame(columns=self.index)
        for k, v in self.index.items():
            for i in v:
                try:
                    new_df[k] = df[i]
                except KeyError:
                    continue
        if self.donor is None:
            new_df["Donor"] = self.donor

        new_df = new_df.replace("-", np.nan)
        self.final_df = new_df
        self.co2_type_converter()
        return self.final_df

    def co2_type_converter(self):
        """
        input: pd.DataFrame
        Generates a new columns containing elements compatible with co2 calculator
        :return: csv file
        """

        df = self.final_df
        df['Type_calc'] = df["Type"].map(self.types).fillna('Others')
        self.final_df = df
        self.final_df.to_csv('uploads/final_df.csv', index=False)

    def sql_tables(self):
        """
        :input: final common dataframe
        :output: separated tables
        """
        Device = self.final_df[["Serial Number", "Type", "Brand", "Model", "Processor", "RAM", "HDD", "Display",
                                 "Weight", "TypeCalculator", "Quantity"]]
        DeviceDonor = self.final_df[["Donor", "Serial Number"]].reset_index()
        DeviceDonor = DeviceDonor.rename(columns={'index': "DonorID"})
        Reference = self.final_df[["Serial Number", "Asset Tag", "Reference"]]
        DeviceStatus = self.final_df[["Serial Number", "Grade", "Defects", "Disk Status"]]

        Device.to_csv("uploads/Device.csv", index=False)
        DeviceDonor.to_csv("uploads/DeviceDonor.csv", index=False)
        Reference.to_csv("uploads/Reference.csv", index=False)
        DeviceStatus.to_csv("uploads/DeviceStatus.csv", index=False)
        