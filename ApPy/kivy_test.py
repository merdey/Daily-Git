import datetime, pickle, os
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
        date = datetime.datetime.now()
        self.date = [date.month, date.day, date.year]
        self.notes = notes

    def changeStatus(self, new_status):
        assert status in valid_status_options, 'Invalid Status'
        
        self.status = new_status

    def summary(self):
        #returns summary string for kivy
        s = '{0}    {1}    {2}'.format(self.company_name, self.status, self.interest)
        return s

    def __str__(self):
        #full string representation when using CLI
        s = 'Company Name: {0}\nStatus: {1}\nDate: {2}/{3}/{4}\nInterest: {5}\nURL: {6}\n{7}\n'.format(self.company_name, self.status, self.date[0], self.date[1], self.date[2], self.interest, self.url, self.category)
        if self.notes:
            s += self.notes + '\n'
        return s

class ApplicationList:
    def __init__(self, filename = ''):
        if filename:
            path = os.path.dirname(os.path.abspath(__file__))
            #read in data from filename, adds each job application to self.apps
            with open(path + '\\' + filename, 'rb') as f:
                self.apps = pickle.load(f).apps
                print(self)
        else:
            self.apps = []

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
        #full string representation when using CLI
        s = ''
        for app in self.apps:
            s += (str(app) + '\n')
        return s

#playing with kivy
from kivy.uix.listview import ListView
from kivy.base import runTouchApp

appList = ApplicationList('apps.txt')
appList.sort(DEFAULT_SORT, True) #defaults to listing companies by interest from highest to lowest

class MainView(ListView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(
            item_strings=[app.summary() for app in appList.apps])

if __name__ == '__main__':
    runTouchApp(MainView())
