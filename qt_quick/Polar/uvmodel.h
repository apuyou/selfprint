#ifndef UVMODEL_H
#define UVMODEL_H

#include <QAbstractListModel>
#include <QStringList>

class UV
{
public:
    UV(const QString &nom, const int nbPages);

    QString nom() const;
    int nbPages() const;

private:
    QString m_nom;
    int m_nbPages;
};

class UVModel : public QAbstractListModel
{
    Q_OBJECT
public:
    enum AnimalRoles {
        DisplayRole,
        SizeRole
    };

    UVModel(QObject *parent = 0);

    Q_INVOKABLE void addUV(const QString &nom, const int nbPages);

    int rowCount(const QModelIndex & parent = QModelIndex()) const;

    QVariant data(const QModelIndex & index, int role = Qt::DisplayRole) const;

private:
    QList<UV> m_uvs;
};

#endif // UVMODEL_H
