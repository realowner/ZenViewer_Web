

class ThreadNum:

    def how_many_threads(views_num):
        
        figs = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        for fig in figs:
            res = views_num % fig

            if res == 0:
                return fig