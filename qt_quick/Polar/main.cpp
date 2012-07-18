#include <QtGui/QApplication>
#include <Qt/qsortfilterproxymodel.h>
#include <QDeclarativeContext>
#include "qmlapplicationviewer.h"
#include "uvmodel.h"

Q_DECL_EXPORT int main(int argc, char *argv[])
{
    QScopedPointer<QApplication> app(createApplication(argc, argv));

    UVModel *uvmodel = new UVModel();
    QSortFilterProxyModel *proxymodel = new QSortFilterProxyModel();
    proxymodel->setSourceModel(uvmodel);

    QmlApplicationViewer viewer;
    viewer.setOrientation(QmlApplicationViewer::ScreenOrientationAuto);
    viewer.rootContext()->setContextProperty("modelUVs", uvmodel);
    viewer.rootContext()->setContextProperty("filteredUVs", proxymodel);
    viewer.setMainQmlFile(QLatin1String("qml/Polar/main.qml"));
    viewer.showExpanded(); //viewer.showFullScreen();

    return app->exec();
}
