
from PyQt5 import QtWidgets
from Main import Ui_MainWindow
import qtmodern.styles
import qtmodern.windows

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  ui = Ui_MainWindow()
  ui.setupUi(MainWindow)
  ui.statusbar.setSizeGripEnabled(False)
  qtmodern.styles.dark(app)
  mw = qtmodern.windows.ModernWindow(MainWindow)
  qr = mw.frameGeometry()
  cp = QtWidgets.QDesktopWidget().availableGeometry().center()
  qr.moveCenter(cp)
  mw.move(qr.topLeft())
  mw.show()
  sys.exit(app.exec_())
