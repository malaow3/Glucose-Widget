/*
    file:           bggraph.js
    fileOverview:   Large widget script
*/

// Replace url with your repl link
const url = "https://example.myaccount.repl.co"
let req = new Request(url)
let res = await req.loadJSON()

if (config.runsInWidget) {
    let widget = await createWidget(res.bg, "#212121")
    Script.setWidget(widget)      
    Script.complete()
}

async function createWidget(pretitle, color) {
    let w = new ListWidget()
    w.backgroundColor = new Color(color)
    let item = "               " + pretitle
    let preTxt = w.addText(item)
    preTxt.textColor = Color.white()
    preTxt.centerAlignText()
    preTxt.font = Font.systemFont(42)

    w.addSpacer(1)
    let imgReq = new Request("https://example.myaccount.repl.co/plot.png")
    let img = await imgReq.loadImage()
    let wimg = w.addImage(img)
    wimg.rightAlignImage()
    wimg.imageSize = new Size(450, 255)
    w.centerAlignContent
    w.setPadding(0, 0, 0, 0)
  
    return w
}