from app.models import Settings


class ThreadNum:

    def how_many_threads(views_num):

        max_thr = Settings.query.get(1).thr_num
        
        figs = [i for i in range(1, max_thr+1)]

        for fig in figs:
            res = views_num % fig

            if res == 0:
                return fig