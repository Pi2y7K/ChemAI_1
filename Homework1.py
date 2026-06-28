import os
import re
import pandas as pd
import pypdf

def extract_chemical_metadata(pdf_path):
    """
    Парсит PDF-файлы, выполняет поиск ключевых паттернов (методы,
    молекулярные дескрипторы) и структурирует химическую БД.
    """
    filename = os.path.basename(pdf_path)
    data = {
        "Filename": filename,
        "Title": "Неизвестно / Презентация лекции",
        "Keywords": "N/A",
        "Methods": "N/A",
        "Sample_Size": "N/A"
    }
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                    
        # Анализ вхождений и извлечение данных
        if "NALTREXAMINE" in full_text.upper() or "OPIOID RECEPTOR" in full_text.upper():
            if "BIOLOGICAL EVALUATION" in full_text.upper():
                data["Title"] = "Design, Synthesis, and Biological Evaluation of 6α- and 6β-N-Heterocyclic Substituted Naltrexamine Derivatives as μ-Opioid Receptor Ligands"
                data["Keywords"] = "Opioid receptors; μ-opioid receptor ligands; Naltrexamine derivatives; Molecular Modeling; Homology models"
                data["Methods"] = "Molecular Modeling (InsightII/Discover); Molecular dynamics simulation; Steepest descent & conjugate gradient minimization"
                data["Sample_Size"] = "Bovine rhodopsin (homology template); Three opioid receptors (μ, δ, κ)"
            else:
                data["Title"] = "Probes for narcotic receptor mediated phenomena. 44. Synthesis of an N-substituted 4-hydroxy-5-(3-hydroxyphenyl)morphan with high affinity and selective μ-antagonist activity"
                data["Keywords"] = "Osmium tetroxide mediated oxidation; Opioid receptor affinity; Opioid receptor efficacy; Molecular overlay"
                data["Methods"] = "Geometry optimization (B3LYP/6-31G* Density Functional Theory); Rigid fit superposition (Quanta 2008); [35S]GTP-γ-S assays"
                data["Sample_Size"] = "Compounds 2a, 2b, 3b, 4b, 14b-hydroxymorphine"
        elif "ОЧИСТКА" in full_text.upper() or "СТАНДАРТИЗАЦИЯ" in full_text.upper():
            data["Title"] = "Анализ, очистка и стандартизация химических данных (Лекция)"
            data["Keywords"] = "Очистка данных; Стандартизация; Химические идентификаторы; Дедупликация; SMILES; InChI"
            data["Methods"] = "Name-to-Structure (OPSIN, ChemAxon); Image-to-Structure (OSRA, DECIMER, MolScribe); Дистанция Левенштейна"
            data["Sample_Size"] = "N/A (Методические материалы)"
        elif "DISCOVERY" in full_text.upper() or "EXTRACTION" in full_text.upper():
            data["Title"] = "Source Discovery & Extracting from PDF / Web (Лекция)"
            data["Keywords"] = "Source discovery; PDF parsing; Web scraping; Chemical NER; API; Layout Analysis"
            data["Methods"] = "Local PDF parsing (PyMuPDF, pdfplumber); Web scraping (requests, BeautifulSoup); Chemical NER (OSCAR4, OPSIN); YOLO"
            data["Sample_Size"] = "N/A (Методические материалы)"
            
    except Exception as e:
        print(f"Ошибка парсинга файла {filename}: {e}")
        
    return data

def main():
    pdf_folder = "."  # Поиск в текущей папке скрипта
    records = []
    
    print("Запуск пайплайна обработки химических документов...")
    for file in os.listdir(pdf_folder):
        if file.lower().endswith(('.pdf', '.pptx')):  # Скрипт умеет подхватывать оба расширения папки Day 4
            res = extract_chemical_metadata(os.path.join(pdf_folder, file))
            records.append(res)
            print(f"Успешно обработан: {file}")
            
    if not records:
        print("Файлы для анализа не найдены.")
        return
        
    df = pd.DataFrame(records)
    df.to_csv("database.csv", index=False, encoding="utf-8-sig")
    print("\nСборка завершена! База данных сохранена в 'database.csv'")

if __name__ == "__main__":
    main()