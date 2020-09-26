/*
    file:           bggraph2.js
    fileOverview:   Medium widget script
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
    let item = "                         " + pretitle
    let preTxt = w.addText(item)
    preTxt.textColor = Color.white()
    preTxt.font = Font.systemFont(32)
  
    let imgReq = new Request("https://example.myaccount.repl.co/plot2.png")
    let img = await imgReq.loadImage()
    let wimg = w.addImage(img)
    wimg.centerAlignImage()
    wimg.imageSize = new Size(400, 90)

    return w
}