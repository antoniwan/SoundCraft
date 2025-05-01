package main

import (
	"fmt"
	"os"

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
}

func initialModel() model {
	return model{
		choices: []string{"Show Greeting", "Exit Program"},
		selected: -1,
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

	if m.selected != -1 && m.choices[m.selected] == "Show Greeting" {
		s += "\n" + titleStyle.Render("HELLO SOUNDCRAFTER!") + "\n"
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
