import os, utils


class Runner(object):
    def __init__(self, *args):
        if args[0] == '' or args[0] == 'tests':
            self.test_scope = 'tests'
        else:
            self.test_scope = args[0]
        Runner.clear_config_yaml()

    # the enter point for run the tests
    def run_test(self):
        utils.generate_results(self.test_scope)
        utils.generate_html_report()

    @staticmethod
    def clear_config_yaml():
        config_yaml_path = os.getcwd() + '/configs/temp.yaml'
        try:
            os.remove(config_yaml_path)
        except OSError:
            pass
        print('start to init the temp file')
        open(config_yaml_path, 'w+')


def runner():
    run = Runner('tests')
    run.run_test()


if __name__ == '__main__':
    runner()
