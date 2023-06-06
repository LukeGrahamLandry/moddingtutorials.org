// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Modding Tutorials',
  tagline: 'Make Minecraft mods with Forge',
  url: 'https://moddingtutorials.org',
  baseUrl: '/',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  favicon: '/img/icon.png',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./scripts/sidebars.js'),
          editUrl: ({locale, versionDocsDirPath, docPath}) => {
            if (docPath.startsWith("mods")) return undefined;
            if (docPath.startsWith("mirror")) return undefined;
            if (docPath.startsWith("wrapperlib")) return `https://github.com/LukeGrahamLandry/WrapperLib/wiki`;
           
            return `https://github.com/LukeGrahamLandry/moddingtutorials.org/edit/main/docs/${docPath}`;
          },
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        logo: {
          alt: 'Logo',
          src: '/img/icon.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'MC Forge',
          },
          {to: 'pathname:///commissions.html', label: '💰Commissions', position: 'left'},
          {
            href: 'https://discord.com/invite/uG4DewBcwV',
            label: 'Discord Server',
            position: 'right',
          },
          {
            href: 'https://github.com/LukeGrahamLandry',
            label: 'Github',
            position: 'right',
          },
        ],
      },
      footer: {
        links: [
          {
            html: `
            <style>
              .alert {
                font-weight: bolder;
                border-radius: 5px;
                text-align: center;
                border: 4px solid;
                display: inline-block;
              }
              .full {
                font-size: 2rem;
                width: 100%;
                max-width: 800px;
                padding-top: 10px;
                padding-bottom: 10px;
              }
              .blue {
                color: #060e30 !important;
                background-color: #5865F2 !important;
                border-color: #7289DA;
              }
            </style>
            <a class="alert blue full" href="/discord" target="_blank"> Got Questions? Join the Discord Server! </a>`
          }
        ],
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['java']
      },
    }),
};

module.exports = config;
