import datetime, pickle
from operator import attrgetter

valid_status_options = ['interested',
                        'researched',
                        'applied',
                        'phone screen',
                        'interview',
                        'offer',
                        ]

#mainly to ensure categories maintain some sense of order (for sorting) and to act as a spell/sanity check when inputting new apps
valid_categories = ['Varied', #alias for "I'm not quite sure"
                    'Web',
                    'iOS',
                    'Telecom',
                    'Education',
                    'Data',
                    'Games',
                    'Business',
                    ]

DEFAULT_SORT = 'interest'

class JobApplication:
    def __init__(self, company_name, status, interest, url, category, notes=''):
        assert status in valid_status_options, 'Invalid Status'
        assert category in valid_categories, 'Invalid category: check spelling or ammend the list of valid categories'
        
        self.company_name = company_name
        self.status = status
        self.interest = interest
        self.url = url
        self.category = category
        self.date = datetime.datetime.now()
        self.date = [self.date.month, self.date.day, self.date.year]
        self.notes = notes

    def changeStatus(self, new_status):
        assert status in valid_status_options, 'Invalid Status'
        
        self.status = new_status

    def __str__(self):
        s = 'Company Name: {0}\nStatus: {1}\nDate: {2}/{3}/{4}\nInterest: {5}\nURL: {6}\n{7}\n'.format(self.company_name, self.status, self.date[0], self.date[1], self.date[2], self.interest, self.url, self.category)
        if self.notes:
            s += self.notes + '\n'
        return s

class ApplicationList:
    def __init__(self, filename = ''):
        self.apps = []
        if filename:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                for app in data.apps:
                    self.add(app)
                f.close()

    def add(self, application):
        self.apps.append(application)

    def remove(self, company_name):
        #removes app based on app.company_name, may add ability to remove based on more factors
        self.apps = [app for app in self.apps if app.company_name != company_name]

    def search(self, key, value):
        found = []
        k = attrgetter(key)
        for app in self.apps:
            if k(app) == value:
                found.append(app)
        return found

    def sort(self, sort_key, reverse=False):
        #sorts self.apps by key
        self.apps.sort(key=attrgetter(sort_key))
        if reverse:
            self.apps = self.apps[::-1]

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def __str__(self):
        #string rep when using as CLI
        s = ''
        for app in self.apps:
            s += (str(app) + '\n')
        return s

appList = ApplicationList('apps.txt')
appList.sort(DEFAULT_SORT, True) #defaults to listing companies by interest from highest to lowest
print(str(appList))

#test search
results = appList.search('company_name', 'Test5')
if results:
    for result in results:
        print(str(result) + '\n')
else:
    print('No applications match that search')

appList.save('apps.txt')






