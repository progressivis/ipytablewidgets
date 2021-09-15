// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021, v0.1.0

/*
 NB: Parts of this file adapted  from Jupyter Widgets (https://github.com/jupyter-widgets/ipywidgets/blob/master/ui-tests/tests/widgets.test.ts)
     Copyright (c) 2015 Project Jupyter Contributors
     All rights reserved.

     Redistribution and use in source and binary forms, with or without
     modification, are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice, this
     	list of conditions and the following disclaimer.

     2. Redistributions in binary form must reproduce the above copyright notice,
     	this list of conditions and the following disclaimer in the documentation
   	and/or other materials provided with the distribution.

     3. Neither the name of the copyright holder nor the names of its
     contributors may be used to endorse or promote products derived from
     this software without specific prior written permission.

     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import { galata, describe, test } from '@jupyterlab/galata';
import * as path from 'path';

jest.setTimeout(100000);

describe('End to end test', () => {
  beforeAll(async () => {
    await galata.resetUI();
    galata.context.capturePrefix = 'end2end';
  });

  afterAll(async () => {
    galata.context.capturePrefix = '';
  });

  test('Upload files to JupyterLab', async () => {
    await galata.contents.moveDirectoryToServer(
      path.resolve(__dirname, `./notebooks`),
      'uploaded'
    );
    expect(
      await galata.contents.fileExists('uploaded/end2end.ipynb')
    ).toBeTruthy();
  });

  test('Refresh File Browser', async () => {
    await galata.filebrowser.refresh();
  });

  test('Open directory uploaded', async () => {
    await galata.filebrowser.openDirectory('uploaded');
    expect(
      await galata.filebrowser.isFileListedInBrowser('end2end.ipynb')
    ).toBeTruthy();
  });

  test('Run notebook end2end.ipynb and capture cell outputs', async () => {
    const notebook = 'end2end.ipynb';
    await galata.notebook.open(notebook);
    expect(await galata.notebook.isOpen(notebook)).toBeTruthy();
    await galata.notebook.activate(notebook);
    expect(await galata.notebook.isActive(notebook)).toBeTruthy();

    let numCellImages = 0;

    const getCaptureImageName = (id: number): string => {
      return `cell-${id}`;
    };

    await galata.notebook.runCellByCell({
      onAfterCellRun: async (cellIndex: number) => {
        const cell = await galata.notebook.getCellOutput(cellIndex);
	console.log("CELL:", cell);
        if (cell) {
          if (
            await galata.capture.screenshot(
              getCaptureImageName(numCellImages),
              cell
            )
          ) {
            numCellImages++;
          }
        }
      },
    });

    for (let c = 0; c < numCellImages; ++c) {
      expect(
        await galata.capture.compareScreenshot(getCaptureImageName(c))
      ).toBe('same');
    }
  });

  test('Close notebook end2end.ipynb', async () => {
    await galata.notebook.close(true);
  });

});
