#include "uvmodel.h"
#include <stdio.h>
#include <stdlib.h>

UV::UV(const QString &nom, const int nbPages)
    : m_nom(nom), m_nbPages(nbPages)
{
}

QString UV::nom() const
{
    return m_nom;
}

int UV::nbPages() const
{
    return m_nbPages;
}

UVModel::UVModel(QObject *parent)
    : QAbstractListModel(parent)
{
    QHash<int, QByteArray> roles;
    roles[DisplayRole] = "name";
    roles[SizeRole] = "nbPages";
    setRoleNames(roles);
}

void UVModel::addUV(const QString &nom, const int nbPages)
{
    beginInsertRows(QModelIndex(), rowCount(), rowCount());
    const UV *newuv = new UV(nom, nbPages);
    m_uvs.append(*newuv);
    endInsertRows();
}

int UVModel::rowCount(const QModelIndex & parent) const {
    return m_uvs.count();
}

QVariant UVModel::data(const QModelIndex & index, int role) const {
    if (index.row() < 0 || index.row() > m_uvs.count())
        return QVariant();

    const UV &animal = m_uvs[index.row()];
    if (role == DisplayRole)
        return animal.nom();
    else if (role == SizeRole)
        return animal.nbPages();
    return QVariant();
}
