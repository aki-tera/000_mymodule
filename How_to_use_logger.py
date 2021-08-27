

# PEP8に準拠するとimportが先頭に行くので苦肉の策
while True:
    import sys
    sys.path.append("../000_mymodule/")
    import logger
    from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
    DEBUG_LEVEL = DEBUG
    break


class Test:
    log = logger.Logger("Test", level=DEBUG_LEVEL)

    def __init__(self):
        self.log.debug("__init__")

        self.log.info("Testのインスタンス化")

    def test_sample(self):
        self.log.debug("test_sample")

        self.log.warn("Testのメソッドを実行")


log = logger.Logger("MAIN", level=DEBUG_LEVEL)


def test_function():
    log.debug("test_function")

    log.info("通常の関数を実行")


def main():
    log.debug("main")

    log.info("メインを実行")

    a = Test()
    a.test_sample()

    test_function()


if __name__ == "__main__":
    main()
 
