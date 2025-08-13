import { createSystem, defaultConfig } from "@chakra-ui/react"
import { buttonRecipe } from "./theme/button.recipe"

export const system = createSystem(defaultConfig, {
  globalCss: {
    html: {
      fontSize: "16px",
    },
    body: {
      fontSize: "0.875rem",
      margin: 0,
      padding: 0,
    },
    ".main-link": {
      color: "ui.main",
      fontWeight: "bold",
    },
  },
  theme: {
    tokens: {
      colors: {
        ui: {
          main: { value: "#f43c35" },
        },
        brand: {
          50: { value: "#fee8e7" },
          100: { value: "#fcc5c2" },
          200: { value: "#fa9e9a" },
          300: { value: "#f87771" },
          400: { value: "#f65953" },
          500: { value: "#f43c35" }, // Red Panda primary
          600: { value: "#e6332e" },
          700: { value: "#d42925" },
          800: { value: "#c3201d" },
          900: { value: "#a20e0b" },
        },
      },
    },
    recipes: {
      button: buttonRecipe,
    },
  },
})
