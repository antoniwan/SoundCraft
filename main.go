package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var (
	// Brand colors from builds.software
	titleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFFFFF")).
			Bold(true).
			Padding(0, 1)

	menuItemStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#3D566F")).
			PaddingLeft(2)

	selectedItemStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFDC00")).
			Bold(true).
			PaddingLeft(2)

	footerLineStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#3D566F")).
			Faint(true)

	footerThanksStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFDC00")).
			Bold(true)

	footerQuoteStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#AAAAAA")).
			Italic(true)

	footerLinkStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#0074D9")).
			Underline(true)
)

type model struct {
	choices  []string
	cursor   int
	selected int
	message  string
}

func initialModel() model {
	return model{
		choices: []string{"Show Greeting", "Generate Playlists", "Analyze Project", "Exit Program"},
		selected: -1,
	}
}

func scanAudioFiles() (map[string][]string, error) {
	files := make(map[string][]string)
	
	err := filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		
		if !info.IsDir() {
			ext := strings.ToLower(filepath.Ext(path))
			switch ext {
			case ".mp3":
				files["mp3"] = append(files["mp3"], path)
			case ".wav":
				files["wav"] = append(files["wav"], path)
			case ".mid", ".midi":
				files["midi"] = append(files["midi"], path)
			}
		}
		return nil
	})
	
	return files, err
}

func generatePlaylists() string {
	files, err := scanAudioFiles()
	if err != nil {
		return fmt.Sprintf("Error scanning files: %v", err)
	}

	if len(files) == 0 {
		return "No audio files found in the current directory."
	}

	// Create playlists directory if it doesn't exist
	playlistsDir := "playlists"
	if err := os.MkdirAll(playlistsDir, 0755); err != nil {
		return fmt.Sprintf("Error creating playlists directory: %v", err)
	}

	// Generate timestamp for unique playlist names
	timestamp := time.Now().Format("20060102_150405")
	
	// Generate all audio files playlist
	allFiles := make([]string, 0)
	for _, fileList := range files {
		allFiles = append(allFiles, fileList...)
	}
	
	if len(allFiles) > 0 {
		if err := createM3UPlaylist(filepath.Join(playlistsDir, fmt.Sprintf("all_audio_%s.m3u", timestamp)), allFiles); err != nil {
			return fmt.Sprintf("Error creating all audio playlist: %v", err)
		}
	}

	// Generate type-specific playlists
	for fileType, fileList := range files {
		if len(fileList) > 0 {
			playlistName := fmt.Sprintf("%s_files_%s.m3u", fileType, timestamp)
			if err := createM3UPlaylist(filepath.Join(playlistsDir, playlistName), fileList); err != nil {
				return fmt.Sprintf("Error creating %s playlist: %v", fileType, err)
			}
		}
	}

	// Build result message
	var result strings.Builder
	result.WriteString("\nGenerated playlists:\n\n")
	
	if len(allFiles) > 0 {
		result.WriteString(fmt.Sprintf("All Audio Files: playlists/all_audio_%s.m3u\n", timestamp))
	}
	
	for fileType, fileList := range files {
		if len(fileList) > 0 {
			result.WriteString(fmt.Sprintf("%s Files: playlists/%s_files_%s.m3u\n", 
				strings.ToUpper(fileType), fileType, timestamp))
		}
	}
	
	result.WriteString("\nPlaylists have been created in the 'playlists' directory.\n")
	result.WriteString("You can open these .m3u files with any standard media player.\n")

	return result.String()
}

func createM3UPlaylist(filename string, files []string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write M3U header
	_, err = file.WriteString("#EXTM3U\n")
	if err != nil {
		return err
	}

	// Write each file path
	for _, filePath := range files {
		// Convert to absolute path
		absPath, err := filepath.Abs(filePath)
		if err != nil {
			return err
		}
		
		// Write the file path
		_, err = file.WriteString(absPath + "\n")
		if err != nil {
			return err
		}
	}

	return nil
}

func analyzeProject() string {
	var result strings.Builder
	result.WriteString("\nProject Analysis:\n\n")

	// Get all audio files
	files, err := scanAudioFiles()
	if err != nil {
		return fmt.Sprintf("Error analyzing project: %v", err)
	}

	// Total file counts
	totalFiles := 0
	for _, fileList := range files {
		totalFiles += len(fileList)
	}

	// File type distribution
	result.WriteString("File Type Distribution:\n")
	for fileType, fileList := range files {
		percentage := float64(len(fileList)) / float64(totalFiles) * 100
		result.WriteString(fmt.Sprintf("  %s: %d files (%.1f%%)\n", 
			strings.ToUpper(fileType), len(fileList), percentage))
	}

	// File size analysis
	var totalSize int64
	var largestFile string
	var largestSize int64
	var smallestFile string
	var smallestSize int64 = -1

	for _, fileList := range files {
		for _, file := range fileList {
			info, err := os.Stat(file)
			if err != nil {
				continue
			}
			size := info.Size()
			totalSize += size

			if size > largestSize {
				largestSize = size
				largestFile = file
			}
			if smallestSize == -1 || size < smallestSize {
				smallestSize = size
				smallestFile = file
			}
		}
	}

	// Convert sizes to human-readable format
	formatSize := func(size int64) string {
		const unit = 1024
		if size < unit {
			return fmt.Sprintf("%d B", size)
		}
		div, exp := int64(unit), 0
		for n := size / unit; n >= unit; n /= unit {
			div *= unit
			exp++
		}
		return fmt.Sprintf("%.1f %cB", float64(size)/float64(div), "KMGTPE"[exp])
	}

	result.WriteString("\nFile Size Analysis:\n")
	result.WriteString(fmt.Sprintf("  Total Project Size: %s\n", formatSize(totalSize)))
	result.WriteString(fmt.Sprintf("  Average File Size: %s\n", formatSize(totalSize/int64(totalFiles))))
	result.WriteString(fmt.Sprintf("  Largest File: %s (%s)\n", largestFile, formatSize(largestSize)))
	result.WriteString(fmt.Sprintf("  Smallest File: %s (%s)\n", smallestFile, formatSize(smallestSize)))

	// Directory structure analysis
	var dirCount int
	var fileCount int
	err = filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			dirCount++
		} else {
			fileCount++
		}
		return nil
	})

	if err == nil {
		result.WriteString("\nDirectory Structure:\n")
		result.WriteString(fmt.Sprintf("  Total Directories: %d\n", dirCount))
		result.WriteString(fmt.Sprintf("  Total Files: %d\n", fileCount))
		result.WriteString(fmt.Sprintf("  Audio Files: %d (%.1f%% of total files)\n", 
			totalFiles, float64(totalFiles)/float64(fileCount)*100))
	}

	// Last modified analysis
	var oldestFile string
	var oldestTime time.Time
	var newestFile string
	var newestTime time.Time

	for _, fileList := range files {
		for _, file := range fileList {
			info, err := os.Stat(file)
			if err != nil {
				continue
			}
			modTime := info.ModTime()
			if oldestTime.IsZero() || modTime.Before(oldestTime) {
				oldestTime = modTime
				oldestFile = file
			}
			if newestTime.IsZero() || modTime.After(newestTime) {
				newestTime = modTime
				newestFile = file
			}
		}
	}

	result.WriteString("\nFile Age Analysis:\n")
	result.WriteString(fmt.Sprintf("  Oldest File: %s (%s)\n", 
		oldestFile, oldestTime.Format("2006-01-02 15:04:05")))
	result.WriteString(fmt.Sprintf("  Newest File: %s (%s)\n", 
		newestFile, newestTime.Format("2006-01-02 15:04:05")))
	result.WriteString(fmt.Sprintf("  Project Age: %s\n", 
		time.Since(oldestTime).Round(time.Hour*24).String()))

	return result.String()
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}
		case "down", "j":
			if m.cursor < len(m.choices)-1 {
				m.cursor++
			}
		case "enter", " ":
			m.selected = m.cursor
			switch m.choices[m.selected] {
			case "Exit Program":
				return m, tea.Quit
			case "Generate Playlists":
				m.message = generatePlaylists()
			case "Analyze Project":
				m.message = analyzeProject()
			}
		}
	}

	return m, nil
}

func (m model) View() string {
	s := "\n" + titleStyle.Render("SoundCrafter Menu") + "\n\n"

	for i, choice := range m.choices {
		cursor := "  "
		if m.cursor == i {
			cursor = "> "
		}

		style := menuItemStyle
		if m.cursor == i {
			style = selectedItemStyle
		}

		s += fmt.Sprintf("%s%s\n", cursor, style.Render(choice))
	}

	if m.selected != -1 {
		switch m.choices[m.selected] {
		case "Show Greeting":
			s += "\n" + titleStyle.Render("HELLO SOUNDCRAFTER!") + "\n"
		case "Generate Playlists":
			s += "\n" + m.message + "\n"
		case "Analyze Project":
			s += "\n" + m.message + "\n"
		}
	}

	s += "\nPress q to quit.\n"

	// --- Footer ---
	s += "\n" + footerLineStyle.Render("────────────────────────────────────────────────────────────") + "\n"
	s += footerThanksStyle.Render("Thanks for using SoundCrafter!") + "\n"
	s += footerQuoteStyle.Render("This is my musical core. A ritual space. A structured outlet. A living archive. Welcome to the forge.") + "\n\n"
	s += "" +
		"" + footerLinkStyle.Render("Antonio Rodriguez Martinez (Antoniwan)") + "  |  " +
		footerLinkStyle.Render("https://stronghandssoftheart.com") + "  |  " +
		footerLinkStyle.Render("hello@stronghandssoftheart.com") + "\n"

	return s
}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
