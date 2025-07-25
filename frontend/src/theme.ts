import { createTheme, responsiveFontSizes, ThemeOptions } from '@mui/material/styles';
import { deepmerge } from '@mui/utils';

// Augment the palette to include your custom colors
declare module '@mui/material/styles' {
  interface Palette {
    surface: Palette['primary'];
    surfaceVariant: Palette['primary'];
    onSurface: Palette['primary'];
    outline: Palette['primary'];
  }
  interface PaletteOptions {
    surface?: PaletteOptions['primary'];
    surfaceVariant?: PaletteOptions['primary'];
    onSurface?: PaletteOptions['primary'];
    outline?: PaletteOptions['primary'];
  }
}

// Common theme settings shared between light and dark modes
const commonSettings: ThemeOptions = {
  shape: {
    borderRadius: 8, // Corresponds to --radius: 0.5rem (assuming 1rem = 16px)
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  components: {
    // Example of applying card-hover effect to all cards
    MuiCard: {
      styleOverrides: {
        root: {
          transition: 'transform 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    // Progress bar animation
    MuiLinearProgress: {
        styleOverrides: {
            bar: {
                transition: 'width 0.3s ease'
            }
        }
    }
  },
};

// Function to create a theme based on mode (light/dark)
export const getTheme = (mode: 'light' | 'dark') => {
  let theme = createTheme(deepmerge(commonSettings, {
    palette: {
      mode,
      ...(mode === 'light'
        ? {
            // Palette values for LIGHT mode
            primary: {
              main: 'hsl(207, 90%, 54%)',
              contrastText: 'hsl(211, 100%, 99%)',
            },
            secondary: {
              main: 'hsl(60, 4.8%, 95.9%)',
              contrastText: 'hsl(24, 9.8%, 10%)',
            },
            error: {
              main: 'hsl(0, 84.2%, 60.2%)',
              contrastText: 'hsl(60, 9.1%, 97.8%)',
            },
            warning: {
                main: 'hsl(36, 100%, 56%)',
            },
            success: {
                main: 'hsl(122, 45%, 49%)',
            },
            text: {
              primary: 'hsl(20, 14.3%, 4.1%)',
              secondary: 'hsl(25, 5.3%, 44.7%)',
            },
            background: {
              default: 'hsl(240, 10%, 7.5%)', // Using --surface for the main background
              paper: 'hsl(0, 0%, 100%)',
            },
            divider: 'hsl(20, 5.9%, 90%)',
            // Custom colors
            surface: { main: 'hsl(240, 10%, 7.5%)' },
            surfaceVariant: { main: 'hsl(240, 10%, 11.8%)' },
            onSurface: { main: 'hsl(0, 0%, 87.8%)' },
            outline: { main: 'hsl(240, 3.7%, 27.5%)' },
          }
        : {
            // Palette values for DARK mode
            primary: {
              main: 'hsl(207, 90%, 54%)',
              contrastText: 'hsl(211, 100%, 99%)',
            },
            secondary: {
              main: 'hsl(240, 3.7%, 15.9%)',
              contrastText: 'hsl(0, 0%, 98%)',
            },
            error: {
              main: 'hsl(0, 62.8%, 30.6%)',
              contrastText: 'hsl(0, 0%, 98%)',
            },
            warning: {
                main: 'hsl(36, 100%, 56%)',
            },
            success: {
                main: 'hsl(122, 45%, 49%)',
            },
            text: {
              primary: 'hsl(0, 0%, 98%)',
              secondary: 'hsl(240, 5%, 64.9%)',
            },
            background: {
              default: 'hsl(240, 10%, 3.9%)',
              paper: 'hsl(240, 10%, 7.5%)', // using --surface for paper in dark mode
            },
            divider: 'hsl(240, 3.7%, 15.9%)',
            // Custom colors
            surface: { main: 'hsl(240, 10%, 7.5%)' },
            surfaceVariant: { main: 'hsl(240, 10%, 11.8%)' },
            onSurface: { main: 'hsl(0, 0%, 87.8%)' },
            outline: { main: 'hsl(240, 3.7%, 27.5%)' },
          }),
    },
  }));

  // Apply responsive font sizes
  theme = responsiveFontSizes(theme);
  return theme;
}