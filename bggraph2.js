
// Replace url with your repl link
const url = "https://projectname.youraccount.repl.co"
let imgurl = url + "/testgraph"
let req = new Request(url)
let res = await req.loadJSON()

if (config.runsInWidget) {
  // create and show widget
  let widget = await createWidget(res.bg, "", "", "#212121", imgurl)
  Script.setWidget(widget)

  Script.complete()
} Safari.open("shortcuts://run-shortcut?name=SpringBoard&silent=true")

function createRow(title, number) {
  let row = new UITableRow()
  row.addText(title)
  row.addText(number.toString()).rightAligned()
  return row
}

async function createWidget(pretitle, title, subtitle, color, imgurl) {
  let w = new ListWidget()
  w.addSpacer(null)
  w.backgroundColor = new Color(color)
  let item = "                                    " + pretitle
  let preTxt = w.addText(item)
  preTxt.textColor = Color.white()
  preTxt.rightAlignText()
  preTxt.font = Font.systemFont(30)
  let imgReq = new Request(imgurl)
  let img = await imgReq.loadImage()
  let wimg = w.addImage(img)
  wimg.rightAlignImage()
  wimg.imageSize = new Size(580, 125)
  w.centerAlignContent
  w.setPadding(0, 0, 0, 0)
  return w
}