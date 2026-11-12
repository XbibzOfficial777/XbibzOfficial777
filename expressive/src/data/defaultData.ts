import iconsJson from './icons.json';
import paletteJson from './palette.json';
import type { IconsData, PaletteData } from '../types';
export const ICONS = iconsJson as unknown as IconsData;
export const DEFAULT_PALETTE = paletteJson as unknown as PaletteData;
