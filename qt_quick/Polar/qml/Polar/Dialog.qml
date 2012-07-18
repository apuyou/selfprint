// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: dialog
    width: parent.width*0.65
    height: parent.height*0.9
    color: "#070707"
    radius: 7
    visible: false
    border.width: 3
    border.color: "#606060"
    x: (parent.width-width)/2
    y: (parent.height - height)/2
    property alias titre: titreText.text
    property int tailleTitre: titreText.height + titreText.anchors.topMargin

    MouseArea {
    anchors.fill: parent

        Text {
            id: titreText
            color: "#ffffff"
            font.bold: false
            horizontalAlignment: Text.AlignHCenter
            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0
            font.pixelSize: 30
        }
    }
}
