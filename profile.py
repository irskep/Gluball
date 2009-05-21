import cProfile, pstats, gluball

gluball.profiler = cProfile.Profile()
result = None
try:
    try:
        gluball.profiler = gluball.profiler.run('gluball.profile()')
    except SystemExit:
        pass
except:
    print "fail"
finally:
    gluball.profiler.dump_stats('gluball_profile')

p = pstats.Stats('gluball_profile')
p.sort_stats('cumulative').print_stats(40)
p.strip_dirs().sort_stats(-1).print_stats()