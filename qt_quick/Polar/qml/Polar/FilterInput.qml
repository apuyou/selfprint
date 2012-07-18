// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: rectangle1
    height: champRecherche.height
    color: "#000000"
    radius: 0
    border.width: 2
    border.color: "#ffffff"
    property alias defaultText: mask.text
    property alias validator: champRecherche.validator
    property string filter: ""

    function reset() {
        champRecherche.text = "";
    }

    TextInput {
        id: champRecherche
        height: 40
        color: "#ffffff"
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 6
        anchors.verticalCenter: parent.verticalCenter
        z: 1
        horizontalAlignment: TextInput.AlignLeft
        inputMask: ""
        cursorVisible: true
        selectedTextColor: "#000000"
        font.pixelSize: 25
        focus: true
        onTextChanged: {
            if (text != "") {
                mask.color = "#00ffffff"
            }
            else
            {
                mask.color = "#ffffff"
            }
            filter = qsTr(text);
        }
    }

    Text {
        id: mask
        y: 0
        color: "#ffffff"
        text: qsTr("Filter")
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 5
        anchors.verticalCenter: parent.verticalCenter
        font.pointSize: 25
    }
}
