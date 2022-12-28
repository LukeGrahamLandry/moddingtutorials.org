import React from 'react';
import Translate, {translate} from '@docusaurus/Translate';
import {PageMetadata} from '@docusaurus/theme-common';
import Layout from '@theme/Layout';

let css = `
.button {
  background-color: #007bff;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
  color: white !important;
  font-weight: bold;
  display: inline-block;
  text-decoration: none;
  cursor: pointer;
  width: 100%;
  max-width: 800px;
  font-size: 1.5rem;
}

.button:hover {
  background-color: blue;
}
`

export default function NotFound() {
  return (
    <>
      <PageMetadata
        title={translate({
          id: 'theme.NotFound.title',
          message: 'Page Not Found',
        })}
      />
      <Layout>
        <main className="container margin-vert--xl">
        <style> {css} </style>
          <div className="row">
            <div className="col col--6 col--offset-3">
              <a href="/" class="button">Minecraft Forge Modding Tutorials</a>
              <a href="/commissions" class="button">Minecraft Mod Commissions</a>
              <h1 className="hero__title">
                <Translate
                  id="theme.NotFound.title"
                  description="The title of the 404 page">
                  Page Not Found
                </Translate>
              </h1>
              <p>
                <Translate
                  id="theme.NotFound.p1"
                  description="The first paragraph of the 404 page">
                  We could not find what you were looking for.
                </Translate>
              </p>
              <p>
                <Translate
                  id="theme.NotFound.p2"
                  description="The 2nd paragraph of the 404 page">
                  Please contact the owner of the site that linked you to the
                  original URL and let them know their link is broken.
                </Translate>
              </p>
            </div>
          </div>
        </main>
      </Layout>
    </>
  );
}
