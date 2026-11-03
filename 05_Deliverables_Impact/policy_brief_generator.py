from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime

class PolicyBriefPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Qonnect GeoAI - Agricultural Intelligence Policy Brief', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.date.today()}', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_policy_pdf(output_file="05_Deliverables_Impact/Qonnect_Policy_Brief.pdf"):
    pdf = PolicyBriefPDF()
    pdf.add_page()
    
    data = [
        {"parcel_id": 1, "crop": "Durum Wheat", "status": "Optimal", "yield": 130.61, "action": "None required"},
        {"parcel_id": 2, "crop": "Highland Barley", "status": "High Stress", "yield": 65.82, "action": "Immediate irrigation required"}
    ]
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '1. Executive Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    summary = ("This brief provides an automated assessment of crop health and yield predictions "
               "for the Sinana Woreda in Bale, Oromia. Using Sentinel-2 satellite imagery and "
               "GeoAI modeling, regional food security risks have been identified.")
    pdf.multi_cell(0, 8, summary)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '2. Regional Findings & Impact', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f"- Total Monitored Farms: 2 parcels", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"- High Stress Zones Detected: 1 parcel (Requires Intervention)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"- Total Predicted Yield: 196.43 Quintals", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, '3. Parcel-Level Interventions', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 10)
    
    for item in data:
        pdf.cell(0, 8, f"Parcel ID: {item['parcel_id']} | Crop: {item['crop']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 8, f"Status: {item['status']} | Predicted Yield: {item['yield']} Quintals", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(255, 0, 0) if item['status'] == "High Stress" else pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 8, f"Required Action: {item['action']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
    pdf.output(output_file)
    print(f"Policy Brief successfully saved to {output_file}")

if __name__ == "__main__":
    generate_policy_pdf()
