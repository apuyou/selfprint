// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item {
    id: buton
    property alias text: label.text
    property alias textSize: label.font.pixelSize
    signal clicked
    width: label.width + 2*10
    height: label.height + 2*10

    Rectangle {
        id: rect
        color: "#ffffff"
        smooth: true; radius: 7
        anchors.rightMargin: border.width/2
        anchors.leftMargin: border.width/2
        anchors.bottomMargin: border.width/2
        anchors.topMargin: border.width/2
        anchors.fill: parent
        clip: false
        border {color: "#B9C5D0"; width: 4}

        MouseArea {
            anchors.fill: parent
            id: mouseArea
        }
        Text {
            id: label
            x: 54
            y: 79
            text: "Button"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 30
            color: "#ffffff"
        }
    }
    Component.onCompleted: {
        mouseArea.clicked.connect(clicked)
    }
    states: [
        State {
            name: "ok"

            PropertyChanges {
                target: rect
                color: "#005412"
                border.color: Qt.lighter(color)
            }
        },
        State {
            name: "cancel"
            PropertyChanges {
                target: rect
                color: "#660606"
                border.color: Qt.lighter(color)
            }
        },
        State {
            name: "insensitive"
            PropertyChanges {
                target: rect
                color: "#777777"
                border.color: Qt.darker(color)
            }
            PropertyChanges {
                target: mouseArea
                enabled: false
            }
        }
    ]
}
// but : donner le texte, la taille du texte, le type du bouton (ok/cancel)
// et le code se débrouille de mettre la couleur du bouton et de la bordure
// le texte et renvoie un truc quand on clique
