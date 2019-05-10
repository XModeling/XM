from matplotlib import pyplot as plt
import numpy as np

##plt.switch_backend('TkAgg')
class MarkerUpdater:
    def __init__(self):
        ##for storing information about Figures and Axes
        self.figs = {}

        ##for storing timers
        self.timer_dict = {}

    def add_ax(self, ax, features=[]):
        ax_dict = self.figs.setdefault(ax.figure,dict())
        ax_dict[ax] = {
            'xlim' : ax.get_xlim(),
            'ylim' : ax.get_ylim(),
            'figw' : ax.figure.get_figwidth(),
            'figh' : ax.figure.get_figheight(),
            'scale_s' : 1.0,
            'scale_a' : 1.0,
            'features' : [features] if isinstance(features,str) else features,
        }
        ax.callbacks.connect('xlim_changed' and 'ylim_changed', self.update_axes)
        #ax.figure.canvas.mpl_connect('resize_event', self.update_axes)

    def update_axes(self, event):
        #print("Hello")
        for fig,axes in self.figs.items():
            #if fig is event.canvas.figure:

                for ax, args in axes.items():
                    ##make sure the figure is re-drawn
                    update = True

                    fw = fig.get_figwidth()
                    fh = fig.get_figheight()
                    fac1 = min(fw/args['figw'], fh/args['figh'])


                    xl = ax.get_xlim()
                    yl = ax.get_ylim()
                    fac2 = min(
                        abs(args['xlim'][1]-args['xlim'][0])/abs(xl[1]-xl[0]),
                        abs(args['ylim'][1]-args['ylim'][0])/abs(yl[1]-yl[0])
                    )

                    ##factor for marker size
                    facS = (fac1*fac2)/args['scale_s']

                    ##factor for alpha -- limited to values smaller 1.0
                    facA = min(1.0,fac1*fac2)/args['scale_a']

                    ##updating the artists
                    if facS != 1.0:
                        for line in ax.lines:
                            if 'size' in args['features']:
                                line.set_markersize(line.get_markersize()*facS)

                            if 'alpha' in args['features']:
                                alpha = line.get_alpha()
                                if alpha is not None:
                                    line.set_alpha(alpha*facA)


                        for path in ax.collections:
                            if 'size' in args['features']:
                                path.set_sizes([s*facS**2 for s in path.get_sizes()])

                            if 'alpha' in args['features']:
                                alpha = path.get_alpha()
                                if alpha is not None:
                                    path.set_alpha(alpha*facA)

                        args['scale_s'] *= facS
                        args['scale_a'] *= facA

                self._redraw_later(fig)



    def _redraw_later(self, fig):
        timer = fig.canvas.new_timer(interval=10)
        timer.single_shot = True
        timer.add_callback(lambda : fig.canvas.draw_idle())
        timer.start()

        ##stopping previous timer
        if fig in self.timer_dict:
            self.timer_dict[fig].stop()

        ##storing a reference to prevent garbage collection
        self.timer_dict[fig] = timer


def func():
    my_updater = MarkerUpdater()

    ##setting up the figure
    fig, axes = plt.subplots(nrows = 2, ncols =2)#, figsize=(1,1))
    ax1,ax2,ax3,ax4 = axes.flatten()

    ## a line plot
    x1 = np.linspace(0,np.pi,30)
    y1 = np.sin(x1)
    ax1.plot(x1, y1, 'ro', markersize = 10, alpha = 0.8)
    ax3.plot(x1, y1, 'ro', markersize = 10, alpha = 1)

    ## a scatter plot
    x2 = np.random.normal(1,1,30)
    y2 = np.random.normal(1,1,30)
    ax2.scatter(x2,y2, c = 'b', s = 100, alpha = 0.6)

    ## scatter and line plot
    ax4.scatter(x2,y2, c = 'b', s = 100, alpha = 0.6)
    ax4.plot([0,0.5,1],[0,0.5,1],'ro', markersize = 10) ##note: no alpha value!

    ##setting up the updater
    #my_updater.add_ax(ax1, ['size'])  ##line plot, only marker size
    #my_updater.add_ax(ax2, ['size'])  ##scatter plot, only marker size
    #my_updater.add_ax(ax3, ['alpha']) ##line plot, only alpha
    #my_updater.add_ax(ax4, ['size', 'alpha']) ##scatter plot, marker size and alpha

    return fig

if __name__ == '__main__':
    fig = func()
    my_updater = MarkerUpdater()
    for ax in fig.axes:
        my_updater.add_ax(ax, ['size'])