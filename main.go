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
		choices: []string{"Show Greeting", "Generate Playlists", "Exit Program"},
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
			style = select