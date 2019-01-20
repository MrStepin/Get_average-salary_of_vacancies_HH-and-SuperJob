import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os

PARAMETERS_HH = {"search_period": "30", "area": "1"}
SUPERJOB_URL_API = "https://api.superjob.ru/2.0/vacancies/"
LIST_OF_NAMES_OF_VACANCIES = ["Программист Python", 
                              "Программист C#", 
                              "Программист Java", 
                              "Программист С++", 
                              "Программист Java Script" ]

def get_average_salary_hh(PARAMETERS_HH, LIST_OF_NAMES_OF_VACANCIES):
    print("Пожалуйста подождите, идет обработка вакансий c HeadHunter.")
    list_with_all_data = []
    for name_of_vacancy in LIST_OF_NAMES_OF_VACANCIES:  
        hh_api_url_for_get_total_pages= "https://api.hh.ru/vacancies?text={}".format(name_of_vacancy)
        response_total_pages = requests.get(hh_api_url_for_get_total_pages, params = PARAMETERS_HH)
        total_pages = int(response_total_pages.json().get("pages"))
        total_vacancies = response_total_pages.json().get("found") 

        list_with_vacancies = []
        for current_page in range(total_pages):
            hh_api_url = "https://api.hh.ru/vacancies?text={}&clusters=true&enable_snippets=true&page={}".format(name_of_vacancy, current_page)
            response = requests.get(hh_api_url, params = PARAMETERS_HH)
            list_with_vacancies.append(response.json().get("items"))
        qty_of_pages_in_list = len(list_with_vacancies)	

        list_with_salaries = [] 
        for page_with_vacancies in list_with_vacancies:
            for vacancy in page_with_vacancies:
                info_about_salary = vacancy.get("salary")
                try:
                    if info_about_salary.get("currency") == "RUR":
                        if info_about_salary.get("from") is not None and info_about_salary.get("to") is not None:
                            list_with_salaries.append((int(info_about_salary.get("from"))+int(info_about_salary.get("to")))/2)
                        else:
                            if info_about_salary.get("from") is not None:
                        	    list_with_salaries.append(int(info_about_salary.get("from"))*1.2)
                            else:
                                list_with_salaries.append(int(info_about_salary.get("to"))*0.8)	
                    else: 
                        continue	
                except AttributeError:
                    continue
        qty_of_salaries = int(len(list_with_salaries))
        average_salary = int(sum(list_with_salaries)/qty_of_salaries)

        list_with_all_data.append(total_vacancies)
        list_with_all_data.append(qty_of_pages_in_list)
        list_with_all_data.append(qty_of_salaries)
        list_with_all_data.append(average_salary)

        print("Вакансии {} обработаны!".format(name_of_vacancy))

    return list_with_all_data

def get_average_salary_superjob(SUPERJOB_URL_API, HEADERS, LIST_OF_NAMES_OF_VACANCIES):
    print("Пожалуйста подождите, идет обработка вакансий с SuperJob.")
    parameters = {"town": "4", "keys": "Должность", "page": "0"}
    list_with_all_data = []

    for name_of_vacancy in LIST_OF_NAMES_OF_VACANCIES:  
        parameters["keys"] = name_of_vacancy

        response_total_vacancies = requests.get(SUPERJOB_URL_API, headers = HEADERS, params = parameters)   
        list_of_vacancies = response_total_vacancies.json().get("objects")
        total_vacancies = int(response_total_vacancies.json().get("total"))
        
        if total_vacancies%20 == 0:
            total_pages = total_vacancies//20
        else:
            total_pages = total_vacancies//20 + 1    
        
        list_with_vacancies = []

        for current_page in range(total_pages):
            parameters["page"] = current_page
            response = requests.get(SUPERJOB_URL_API, headers = HEADERS, params = parameters)
            list_with_vacancies.append(response.json().get("objects"))

        qty_of_pages_in_list = len(list_with_vacancies) 

        list_with_salaries = [] 
        for page_with_vacancies in list_with_vacancies:
            for vacancy in page_with_vacancies:
                try:
                    if vacancy.get("currency") == "rub":
                        if vacancy.get("payment_from") != 0 and vacancy.get("payment_to") != 0:
                            list_with_salaries.append((int(vacancy.get("payment_from"))+int(vacancy.get("payment_to")))/2)
                        else:
                            if vacancy.get("payment_from") != 0:
                                list_with_salaries.append(int(vacancy.get("payment_from"))*1.2)
                            else:
                                list_with_salaries.append(int(vacancy.get("payment_to"))*0.8)   
                    else: 
                        continue    
                except AttributeError:
                    continue
        qty_of_salaries = int(len(list_with_salaries))

        average_salary = int(sum(list_with_salaries)/qty_of_salaries)
  
        list_with_all_data.append(total_vacancies)
        list_with_all_data.append(qty_of_pages_in_list)
        list_with_all_data.append(qty_of_salaries)
        list_with_all_data.append(average_salary)

        print("Вакансии {} обработаны!".format(name_of_vacancy))
    
    return list_with_all_data

def print_results_superjob(get_average_salary_superjob):
    
    get_average_salary_superjob.insert(0, "Python")
    get_average_salary_superjob.insert(5, "C#")
    get_average_salary_superjob.insert(10, "Java")
    get_average_salary_superjob.insert(15, "C++")
    get_average_salary_superjob.insert(20, "JavaScript")

    title = "SuperJob Moscow"
    separator = 5 
    list_for_table = [get_average_salary_superjob[element*separator:element*separator+separator] for element in range(len(get_average_salary_superjob)//separator)]
    
    headers_of_table = ["Язык программирования", "Количество вакансий", "Страниц с вакансиями", "Выбрано вакансий для подсчёта", "Средняя зарплата РУБ."]
    list_for_table.insert(0, headers_of_table)
    table = AsciiTable(list_for_table, title)
    print(table.table)

def print_results_hh(get_average_salary_hh):
    
    get_average_salary_hh.insert(0, "Python")
    get_average_salary_hh.insert(5, "C#")
    get_average_salary_hh.insert(10, "Java")
    get_average_salary_hh.insert(15, "C++")
    get_average_salary_hh.insert(20, "JavaScript")

    title = "HeadHunter Moscow"
    separator = 5 
    list_for_table = [get_average_salary_hh[element*separator:element*separator+separator] for element in range(len(get_average_salary_hh)//separator)]
    
    headers_of_table = ["Язык программирования", "Количество вакансий", "Страниц с вакансиями", "Выбрано вакансий для подсчёта", "Средняя зарплата РУБ."]
    list_for_table.insert(0, headers_of_table)
    table = AsciiTable(list_for_table, title)
    print(table.table)

if __name__ == '__main__': 
    load_dotenv()
    secret_key = os.getenv("secret_key")
    HEADERS = {"X-Api-App-Id": secret_key}
    get_average_salary_hh = get_average_salary_hh(PARAMETERS_HH, LIST_OF_NAMES_OF_VACANCIES)
    get_average_salary_superjob = get_average_salary_superjob(SUPERJOB_URL_API, HEADERS, LIST_OF_NAMES_OF_VACANCIES)
    print_results_hh(get_average_salary_hh)
    print_results_superjob(get_average_salary_superjob)
    