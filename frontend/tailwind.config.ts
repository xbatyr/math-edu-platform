import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "hsl(40 26% 96%)",
        foreground: "hsl(217 32% 18%)",
        card: "hsl(0 0% 100%)",
        "card-foreground": "hsl(217 32% 18%)",
        primary: "hsl(15 82% 45%)",
        "primary-foreground": "hsl(40 26% 96%)",
        muted: "hsl(210 20% 94%)",
        "muted-foreground": "hsl(217 12% 42%)",
        border: "hsl(210 22% 84%)",
        ring: "hsl(15 82% 45%)",
      },
      fontFamily: {
        sans: ["Manrope", "sans-serif"],
        serif: ["IBM Plex Serif", "serif"],
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "fade-up": "fade-up .45s ease-out",
      },
    },
  },
  plugins: [],
} satisfies Config;
