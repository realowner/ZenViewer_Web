from app.routes import views
from app import database
from app.models import Settings, CurrentViewer


def start_seed():
    try:
        print('> Settings seeder started')
        settings = Settings(thr_num=10, sec_alg=True)
        database.session.add(settings)
        database.session.commit()
        print('  settings data > DONE')
    except:
        print('  settings data > FAIL')

    try:
        print('> Views seeder started')
        views_seed = CurrentViewer(curr_views=0, need_views=0)
        database.session.add(views_seed)
        database.session.commit()
        print('  views data > DONE')
    except:
        print('  views data > FAIL')

if __name__ == '__main__':
    print('---> SEEDER - START')
    start_seed()
    print('---> SEEDER - DONE')
