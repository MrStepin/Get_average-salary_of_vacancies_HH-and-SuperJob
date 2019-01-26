import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os

HH_API_URL = "https://api.hh.ru/vacancies"
SUPERJOB_URL_API = "https://api.superjob.ru/2.0/vacancies/"
LIST_OF_NAMES_OF_VACANCIES = [ "Python",
                              "C#", 
                              "Java",
                              "C++",
                              "JavaScript"]

def get_list_of_salaries_hh(list_with_vacancies_hh): 
    list_with_salaries = [] 
    for page_with_vacancies in list_with_vacancies_hh:
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
    return list_with_salaries

def get_list_of_salaries_superjob(list_with_vacancies_superjob):
    list_with_salaries = [] 
    for page_with_vacancies in list_with_vacancies_superjob:
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
    return list_with_salaries

def print_results_superjob(list_with_average_salary_superjob):
    
    list_with_average_salary_superjob.insert(0, "Python")
    list_with_average_salary_superjob.insert(5, "C#")
    list_with_average_salary_superjob.insert(10, "Java")
    list_with_average_salary_superjob.insert(15, "C++")
    list_with_average_salary_superjob.insert(20, "JavaScript")

    title = "SuperJob Moscow"
    separator = 5 
    list_for_table = [list_with_average_salary_superjob[element*separator:element*separator+separator] for element in range(len(list_with_average_salary_superjob)//separator)]
    
    headers_of_table = ["Язык программирования", "Количество вакансий", "Страниц с вакансиями", "Выбрано вакансий для подсчёта", "Средняя зарплата РУБ."]
    list_for_table.insert(0, headers_of_table)
    table = AsciiTable(list_for_table, title)
    print(table.table)

def print_results_hh(list_with_average_salary_hh):
    
    list_with_average_salary_hh.insert(0, "Python")
    list_with_average_salary_hh.insert(5, "C#")
    list_with_average_salary_hh.insert(10, "Java")
    list_with_average_salary_hh.insert(15, "C++")
    list_with_average_salary_hh.insert(20, "JavaScript")

    title = "HeadHunter Moscow"
    separator = 5 
    list_for_table = [list_with_average_salary_hh[element*separator:element*separator+separator] for element in range(len(list_with_average_salary_hh)//separator)]
    
    headers_of_table = ["Язык программирования", "Количество вакансий", "Страниц с вакансиями", "Выбрано вакансий для подсчёта", "Средняя зарплата РУБ."]
    list_for_table.insert(0, headers_of_table)
    table = AsciiTable(list_for_table, title)
    print(table.table)



if __name__ == '__main__': 

    load_dotenv()
    secret_key = os.getenv("secret_key")
    HEADERS = {"X-Api-App-Id": secret_key}
    print("Пожалуйста подождите, идет обработка вакансий c HeadHunter.")
    list_with_average_salary_hh = []
    for name_of_vacancy_hh in LIST_OF_NAMES_OF_VACANCIES:  
        parameters_hh = {"text": "Должность", "search_period": "30", "area": "1"}
        parameters_hh["text"] = name_of_vacancy_hh

        response_total_pages_hh = requests.get(HH_API_URL, params = parameters_hh)
        total_pages_hh = int(response_total_pages_hh.json().get("pages"))
        total_vacancies_hh = response_total_pages_hh.json().get("found") 

        list_with_vacancies_hh = []
        parameters_hh_for_get_page = {"text": "Должность", "search_period": "30", "area": "1", "clusters": "true", "enable_snippets": "true", "page": ""}
        parameters_hh_for_get_page["text"] = name_of_vacancy_hh
        for current_page_hh in range(total_pages_hh):
            parameters_hh_for_get_page["page"]= current_page_hh
            response_hh = requests.get(HH_API_URL, params = parameters_hh_for_get_page)
            list_with_vacancies_hh.append(response_hh.json().get("items"))
        qty_of_pages_in_list_hh = len(list_with_vacancies_hh) 
        
        list_of_salaries_hh = get_list_of_salaries_hh(list_with_vacancies_hh)

        qty_of_salaries_hh = int(len(list_of_salaries_hh))
        average_salary_hh = int(sum(list_of_salaries_hh)/qty_of_salaries_hh)

        list_with_average_salary_hh.append(total_vacancies_hh)
        list_with_average_salary_hh.append(qty_of_pages_in_list_hh)
        list_with_average_salary_hh.append(qty_of_salaries_hh)
        list_with_average_salary_hh.append(average_salary_hh)
        print("Вакансии {} обработаны!".format(name_of_vacancy_hh))


    print("Пожалуйста подождите, идет обработка вакансий с SuperJob.")
    parameters = {"town": "4", "keys": "Должность", "page": "0"}
    list_with_average_salary_superjob = []

    for name_of_vacancy_superjob in LIST_OF_NAMES_OF_VACANCIES:  
        parameters["keys"] = name_of_vacancy_superjob

        response_total_vacancies_superjob = requests.get(SUPERJOB_URL_API, headers = HEADERS, params = parameters)   
        list_of_vacancies_superjob = response_total_vacancies_superjob.json().get("objects")
        total_vacancies_superjob = int(response_total_vacancies_superjob.json().get("total"))
        
        if total_vacancies_superjob%20 == 0:
            total_pages_superjob = total_vacancies_superjob//20
        else:
            total_pages_superjob = total_vacancies_superjob//20 + 1    
        
        list_with_vacancies_superjob = []

        for current_page_superjob in range(total_pages_superjob):
            parameters["page"] = current_page_superjob
            response_superjob = requests.get(SUPERJOB_URL_API, headers = HEADERS, params = parameters)
            list_with_vacancies_superjob.append(response_superjob.json().get("objects"))

        qty_of_pages_in_list_superjob = len(list_with_vacancies_superjob) 
        
        list_of_salaries_superjob = get_list_of_salaries_superjob(list_with_vacancies_superjob)

        qty_of_salaries_superjob = int(len(list_of_salaries_superjob))

        average_salary_superjob = int(sum(list_of_salaries_superjob)/qty_of_salaries_superjob)
  
        list_with_average_salary_superjob.append(total_vacancies_superjob)
        list_with_average_salary_superjob.append(qty_of_pages_in_list_superjob)
        list_with_average_salary_superjob.append(qty_of_salaries_superjob)
        list_with_average_salary_superjob.append(average_salary_superjob)

        print("Вакансии {} обработаны!".format(name_of_vacancy_superjob))

    print_results_hh(list_with_average_salary_hh)
    print_results_superjob(list_with_average_salary_superjob)