package main

import (
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

// テンプレートレンダラーの定義
type TemplateRenderer struct {
	templates *template.Template
}

func (t *TemplateRenderer) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

func main() {
	// Echoインスタンスを作成
	e := echo.New()

	// ミドルウェアを追加
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// 環境変数からユーザー名とパスワードを取得
	username := os.Getenv("BASIC_AUTH_USERNAME")
	password := os.Getenv("BASIC_AUTH_PASSWORD")

	// Basic認証を適用
	e.Use(middleware.BasicAuth(func(u, p string, c echo.Context) (bool, error) {
		if u == username && p == password {
			return true, nil
		}
		return false, nil
	}))

	e.Static("/processed_files", "processed_files")

	// テンプレートのレンダラーをセットアップ
	renderer := &TemplateRenderer{
		templates: template.Must(template.ParseGlob("/app/templates/*.html")),
	}
	e.Renderer = renderer

	// アップロードフォームのルート
	e.GET("/", uploadForm)

	// ファイルアップロードのルート
	e.POST("/upload", handleFileUpload)

	// サーバーを開始
	e.Logger.Fatal(e.Start(":8080"))
}

// アップロードフォームを表示
func uploadForm(c echo.Context) error {
	return c.Render(http.StatusOK, "upload.html", nil)
}

// ファイルを処理
func handleFileUpload(c echo.Context) error {
	// フォームからファイルを取得
	file, err := c.FormFile("file")
	if err != nil {
		return err
	}

	src, err := file.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	// ファイルをサーバーに保存
	filePath := filepath.Join("uploaded_files", file.Filename)
	dst, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer dst.Close()

	if _, err = io.Copy(dst, src); err != nil {
		return err
	}

	// Pythonスクリプトを実行
	pythonScript := "python/script.py" // Pythonスクリプトのパスを指定
	cmd := exec.Command("python3", pythonScript, filePath)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("failed to run python script: %v, output: %s", err, string(output))
	}

	// Pythonスクリプトの結果を解析
	volumes, radii, totalVolume, imageWidth, err := parsePythonOutput(string(output))
	if err != nil {
		return err
	}

	// 結果を表示するHTMLをレンダリング
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message":      "File processed successfully",
		"radii":        radii,
		"volumes":      volumes,
		"totalVolume":  totalVolume,
		"imageWidth":   imageWidth, // 横幅のピクセル数を追加
		"processedImg": "processed_files/processed_" + file.Filename,
	})
}

// Pythonの出力を解析する関数
func parsePythonOutput(output string) ([]float64, []float64, float64, int, error) {
	var volumes []float64
	var radii []float64
	var totalVolume float64
	var imageWidth int

	for _, line := range strings.Split(output, "\n") {
		if strings.HasPrefix(line, "radius:") {
			radiusStr := strings.TrimPrefix(line, "radius:")
			radius, err := strconv.ParseFloat(strings.TrimSpace(radiusStr), 64)
			if err != nil {
				return nil, nil, 0, 0, err
			}
			radii = append(radii, radius)
		}
		if strings.HasPrefix(line, "volume:") {
			volumeStr := strings.TrimPrefix(line, "volume:")
			volume, err := strconv.ParseFloat(strings.TrimSpace(volumeStr), 64)
			if err != nil {
				return nil, nil, 0, 0, err
			}
			volumes = append(volumes, volume)
			totalVolume += volume
		}
		if strings.HasPrefix(line, "Image width (in pixels):") {  // 横幅のピクセル数を解析
			widthStr := strings.TrimPrefix(line, "Image width (in pixels):")
			width, err := strconv.Atoi(strings.TrimSpace(widthStr))
			if err != nil {
				return nil, nil, 0, 0, err
			}
			imageWidth = width
		}
	}

	return volumes, radii, totalVolume, imageWidth, nil
}