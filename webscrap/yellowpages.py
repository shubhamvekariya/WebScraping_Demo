import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
url_name = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=San%20Diego%2C%20CA&page="
s_ranges = int(input('Enter starting range:'))
l_ranges = int(input('Enter last range:'))
ids = (s_ranges-1)*30
if s_ranges == 0:
    ids = 0
for k in range(s_ranges, l_ranges):
    url_changed_name = url_name+str(k)
    r = requests.get(url_changed_name)
    soup = BeautifulSoup(r.content, 'html5lib')
    aid = []
    names = []
    reviews = []
    addresses = []
    phones = []
    years = []
    web_links = []
    emails = []
    general_infos = []
    times = []
    payments = []
    categories = []
    neighborhoods = []
    banners = []
    services = []
    other_infos = []
    for all in soup.findAll('div', attrs={'class': 'search-results organic'}):
        all_links = all.findAll('a', attrs={'class': 'business-name'})
        for link in all_links:
            lnk = link.get("href")
            lnk = "https://www.yellowpages.com"+lnk
            r = requests.get(lnk)
            soup = BeautifulSoup(r.content, 'html5lib')
            name = soup.find('div', attrs={'class': 'sales-info'})
            names.append(name.text)
            for c in soup.findAll('a', attrs={'class': 'yp-ratings'}):
                review = c.find('span', attrs={'class': 'count'})
                if review is not None:
                    review = review.text
                else:
                    review = "(0 Review)"
            reviews.append(review)
            address = soup.find('h2', attrs={'class': 'address'})
            addresses.append(address.text)
            phone = soup.find('p', attrs={'class': 'phone'})
            phones.append(phone.text)
            c = soup.find('div', attrs={'class': 'years-in-business'})
            if c is None:
                year = ''
            else:
                year = c.find('div', attrs={'class': 'number'}).text
            years.append(year)
            web_link = ''
            w_link = soup.find('a', attrs={'class': 'secondary-btn website-link'})
            if w_link is not None:
                web_link += w_link.get("href")+'; '
            o_links = soup.findAll('a', attrs={'class': 'other-links'})
            for o_link in o_links:
                if o_link is not None:
                    web_link += o_link.get("href")+'; '
            web_links.append(web_link)
            o_email = ''
            e_link = soup.findAll('a', attrs={'class': 'email-business'})
            for e in e_link:
                if e is not None:
                    email = e.get("href")
                    email = re.sub('mailto:', '', email)
                    o_email += email+"; "
            emails.append(o_email)
            general_info = soup.find('dd', attrs={'class': 'general-info'})
            if general_info is None:
                general_info = ""
            else:
                general_info = general_info.text
            general_infos.append(general_info)
            all_time = soup.find('div', attrs={'class': 'open-details'})
            time = ''
            if all_time is not None:
                for t in all_time.findAll('tr'):
                    l_time = t.find('th', attrs={'class': 'day-label'}).text
                    h_time = t.find('td', attrs={'class': 'day-hours'}).text
                    time += l_time+' '+h_time+'; '
            else:
                time = ''
            times.append(time)
            payment = soup.find('dd', attrs={'class': 'payment'})
            if payment is None:
                payment = ''
            else:
                payment = payment.text
            payments.append(payment)
            category = soup.find('dd', attrs={'class': 'categories'})
            if category is None:
                category = ''
            else:
                category = category.text
            categories.append(category)
            neighborhood = soup.find('dd', attrs={'class': 'neighborhoods'})
            if neighborhood is None:
                neighborhood = ''
            else:
                neighborhood = neighborhood.text
            neighborhoods.append(neighborhood)
            banner = soup.find('dd', attrs={'class': 'banner-ad'})
            if banner is not None:
                banner = banner.find('img')
                if banner is None:
                    banner = ''
                else:
                    banner = banner.get('src')
            else:
                banner = ''
            banners.append(banner)
            service = ''
            o_service = soup.find('section', attrs={'id': 'business-info'})
            c_service = o_service.find('ul')
            if c_service is not None:
                for s in c_service.findAll('li'):
                    service += s.text+'|'
            else:
                n_service = o_service.find('dd', attrs={'class': None})
                if n_service is None:
                    service = ""
                elif '$' in n_service or '$$' in n_service or '$$$' in n_service:
                    service = ""
                else:
                    service = n_service.text
            services.append(service)
            other_info = ''
            o_info = soup.find('dd', attrs={'class': 'other-information'})
            if o_info is not None:
                for p in o_info.findAll('p'):
                    other_info += p.text+';'
            other_info = re.sub('&nbsp', '', other_info)
            other_infos.append(other_info)
            ids += 1
            aid.append(ids)
    df = pd.DataFrame({'ID': aid, 'Restaurant Name': names, 'Review': reviews, 'Address': addresses, 'Phone Number': phones,
                   'Years in Business': years, ' Website Link': web_links, 'Email Address': emails,
                   'General Information': general_infos, 'Time(in Hour)': times, 'Payment Methods': payments,
                   'Category': categories, 'Services/Products': services, 'Neighborhood': neighborhoods,
                   'Banner Link': banners, 'Other Information': other_infos})
    if not os.path.isfile('Restaurants.csv'):
        df.to_csv('Restaurants.csv', index=False, encoding='utf-8')
    else:
        df.to_csv('Restaurants.csv', mode='a', header=False, index=False)
