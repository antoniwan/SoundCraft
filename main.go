package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var (
	titleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF06B7")).
			Bold(true).
			Padding(1, 2)

	menuItemStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFFFFF")).
			PaddingLeft(2)

	selectedItemStyle = lipgloss.NewStyle().
				Foreground(lipgloss.Color("#FF06B7")).
				Bold(true).
				PaddingLeft(2)
)

type model struct {
	choices  []string
	cursor   int
	selected int
}

func initialModel() model {
	return model{
		choices: []string{"Show Greeting", "Exit Program"},
	}
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
			if m.choices[m.selected] == "Exit Program" {
				return m, tea.Quit
			}
		}
	}

	return m, nil
}

func (m model) View() string {
	s := titleStyle.Render("SoundCrafter Menu") + "\n\n"

	for i, choice := range m.choices {
		cursor := " "
		if m.cursor == i {
			cursor = ">"
		}

		style := menuItemStyle
		if m.cursor == i {
			style = selectedItemStyle
		}

		s += fmt.Sprintf("%s %s\n", cursor, style.Render(choice))
	}

	if m.selected != -1 && m.choices[m.selected] == "Show Greeting" {
		s += "\n" + titleStyle.Render("HELLO SOUNDCRAFTER!") + "\n"
	}

	s += "\nPress q to quit.\n"

	return s
}

func main() {
	p := tea.NewProgram(initialModel())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Alas, there's been an error: %v", err)
		os.Exit(1)
	}
}
