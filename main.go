package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"image/color"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
	"gonum.org/v1/plot/vg/draw"
)

var sessionIDURL = "https://share2.dexcom.com/ShareWebServices/Services/General/LoginPublisherAccountByName"
var glucoseURL = "https://share2.dexcom.com/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues?sessionID="
var glucoseGetParams = "&minutes=1440&maxCount=36"

type glucoseJSON struct {
	DT    string `json:"DT"`
	ST    string `json:"ST"`
	Trend int    `json:"Trend"`
	Value int    `json:"Value"`
	WT    string `json:"WT"`
}

var trendMap = map[int]string{
	0: "",
	1: "↑↑",
	2: "↑",
	3: "↗",
	4: "→",
	5: "↘",
	6: "↓",
	7: "↓↓",
	8: " ",
	9: " ",
}

func main() {
	sessionID := getSessionID()
	sessionID = sessionID[1 : len(sessionID)-1]
	fmt.Println(sessionID)
	glucose, trendVal, dataList := getGlucoseData(sessionID)
	trend := trendMap[trendVal]
	finalString := fmt.Sprintf("%d", glucose) + trend
	data := map[string]string{"bg": finalString}
	jsonbytes, _ := json.Marshal(data)
	writeData("output.txt", []byte(string(jsonbytes)))
	writeString := ""
	for index, value := range dataList {
		if index != len(dataList)-1 {
			writeString += fmt.Sprintf("%d", value) + ","
		} else {
			writeString += fmt.Sprintf("%d", value)
		}
	}
	writeData("datalist.txt", []byte(writeString))
	go webServer()

	for true {
		counter := 0
		for counter < 25 {
			glucose, trendVal, dataList := getGlucoseData(sessionID)
			trend := trendMap[trendVal]
			finalString := fmt.Sprintf("%d", glucose) + trend
			data := map[string]string{"bg": finalString}
			jsonbytes, _ := json.Marshal(data)
			writeData("output.txt", []byte(string(jsonbytes)))
			writeString := ""
			for index, value := range dataList {
				if index != len(dataList)-1 {
					writeString += fmt.Sprintf("%d", value) + ","
				} else {
					writeString += fmt.Sprintf("%d", value)
				}
			}
			writeData("datalist.txt", []byte(writeString))
			time.Sleep(30 * time.Second)
			counter++
		}
		sessionID = getSessionID()
	}
}

func getSessionID() string {
	godotenv.Load(".env")
	username := os.Getenv("username")
	password := os.Getenv("password")
	payload := make(map[string]interface{})
	payload["applicationId"] = "d89443d2-327c-4a6f-89e5-496bbb0317db"
	payload["accountName"] = username
	payload["password"] = password
	jsonValue, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", sessionIDURL, bytes.NewBuffer(jsonValue))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "Dexcom Share/3.0.2.11 CFNetwork/672.0.2 Darwin/14.0.0")
	req.Header.Set("Accept", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	body, _ := ioutil.ReadAll(resp.Body)
	return string(body)
}

func getGlucoseData(sessionID string) (int, int, []int) {
	getGlucoseURL := glucoseURL + sessionID + glucoseGetParams

	payload := make(map[string]interface{})
	jsonValue, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", getGlucoseURL, bytes.NewBuffer(jsonValue))
	req.Header.Set("Content-Length", "0")
	req.Header.Set("Accept", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	if resp.StatusCode != 200 {
		getGlucoseData(sessionID)
	}
	body, _ := ioutil.ReadAll(resp.Body)
	results := []glucoseJSON{}
	json.Unmarshal(body, &results)

	data := []int{}
	trend := results[0].Trend
	glucose := results[0].Value

	for _, item := range results {
		data = append(data, item.Value)
	}
	reverseArray(data)
	return glucose, trend, data
}

func reverseArray(list []int) {
	for i, j := 0, len(list)-1; i < j; i, j = i+1, j-1 {
		list[i], list[j] = list[j], list[i]
	}
}

func writeData(filename string, data []byte) {
	err := ioutil.WriteFile(filename, data, 0777)
	// handle this error
	if err != nil {
		// print it out
		fmt.Println(err)
	}
}

func readID(filename string) string {
	data, err := ioutil.ReadFile(filename)
	// if our program was unable to read the file
	// print out the reason why it can't
	if err != nil {
		fmt.Println(err)
	}

	// if it was successful in reading the file then
	// print out the contents as a string
	return (string(data))
}

func webServer() {
	r := gin.Default()

	r.GET("/testgraph", func(c *gin.Context) {

		data := readID("datalist.txt")
		dataList := strings.Split(data, ",")
		p, err := plot.New()
		if err != nil {
			panic(err)
		}
		p.X.Label.Text = ""
		p.Y.Label.Text = "mg/dL"
		p.X.Min = -1
		p.X.Max = float64(len(dataList) + 1)
		p.Y.Min = 40
		p.Y.Max = 405
		p.Add(plotter.NewGrid())
		pts := make(plotter.XYs, len(dataList))
		for i := 0; i < len(dataList); i++ {
			pts[i].X = float64(i)
			pts[i].Y, _ = strconv.ParseFloat(dataList[i], 64)
		}
		s, err := plotter.NewScatter(pts)
		if err != nil {
			panic(err)
		}
		p.BackgroundColor = color.RGBA{33, 33, 33, 255}
		p.X.Color = color.White
		p.X.Label.Color = color.White
		p.Y.Label.Color = color.White
		p.Y.Tick.Color = color.White
		p.Y.Tick.Label.Color = color.White
		p.X.Tick.Label.Color = color.White
		p.X.Tick.Color = color.White
		p.Y.Color = color.White
		s.Color = color.RGBA{255, 105, 180, 255}
		s.Shape = draw.CircleGlyph{}
		s.Radius = 5
		// s.GlyphStyle.Color = color.RGBA{R: 255, B: 128, A: 255}
		p.Add(s)
		if err := p.Save(11*vg.Inch, 4.125*vg.Inch, "points.png"); err != nil {
			panic(err)
		}
		c.File("./points.png")
	})

	r.GET("/", func(c *gin.Context) {

		type outputType struct {
			BG string `json:"bg"`
		}

		data := readID("output.txt")
		result := outputType{}
		json.Unmarshal([]byte(data), &result)
		c.JSON(200, result)
	})

	r.Run()
}
