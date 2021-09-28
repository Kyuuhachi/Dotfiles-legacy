/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

"use strict";

const { MozElements, customElements } = window;

console.log("vtab");

// This is loaded into chrome windows with the subscript loader. Wrap in
// a block to prevent accidentally leaking globals onto `window`.
{
  class VTab extends MozElements.BaseText {
    static get markup() {
      return `
      <stack class="tab-stack" flex="1">
        <vbox class="tab-background">
          <hbox class="tab-line"/>
          <spacer flex="1" class="tab-background-inner"/>
          <hbox class="tab-context-line"/>
        </vbox>
        <hbox class="tab-loading-burst"/>
        <hbox class="tab-content" align="center">
          <stack class="tab-icon-stack">
            <hbox class="tab-throbber" layer="true"/>
            <hbox class="tab-icon-pending"/>
            <image class="tab-icon-image" validate="never" role="presentation"/>
            <image class="tab-sharing-icon-overlay" role="presentation"/>
            <image class="tab-icon-overlay" role="presentation"/>
          </stack>
          <hbox class="tab-label-container"
                onoverflow="this.setAttribute('textoverflow', 'true');"
                onunderflow="this.removeAttribute('textoverflow');"
                flex="1">
            <label class="tab-text tab-label" role="presentation"/>
          </hbox>
          <image class="tab-icon-sound" role="presentation"/>
          <vbox class="tab-label-container proton"
                onoverflow="this.setAttribute('textoverflow', 'true');"
                onunderflow="this.removeAttribute('textoverflow');"
                align="start"
                flex="1">
            <label class="tab-text tab-label" role="presentation"/>
            <hbox class="tab-secondary-label">
              <label class="tab-icon-sound-label tab-icon-sound-playing-label" data-l10n-id="browser-tab-audio-playing2" role="presentation"/>
              <label class="tab-icon-sound-label tab-icon-sound-muted-label" data-l10n-id="browser-tab-audio-muted2" role="presentation"/>
              <label class="tab-icon-sound-label tab-icon-sound-blocked-label" data-l10n-id="browser-tab-audio-blocked" role="presentation"/>
              <label class="tab-icon-sound-label tab-icon-sound-pip-label" data-l10n-id="browser-tab-audio-pip" role="presentation"/>
              <label class="tab-icon-sound-label tab-icon-sound-tooltip-label" role="presentation"/>
            </hbox>
          </vbox>
          <image class="tab-close-button close-icon" role="presentation"/>
        </hbox>
      </stack>
      `;
    }

    static get inheritedAttributes() {
      return {
        ".tab-background": "selected=visuallyselected,fadein,multiselected",
        ".tab-line": "selected=visuallyselected,multiselected,before-multiselected",
        ".tab-loading-burst": "pinned,bursting,notselectedsinceload",
        ".tab-content": "pinned,selected=visuallyselected,titlechanged,attention",
        ".tab-icon-stack": "sharing,pictureinpicture,crashed,busy,soundplaying,soundplaying-scheduledremoval,pinned,muted,blocked,selected=visuallyselected,activemedia-blocked",
        ".tab-throbber": "fadein,pinned,busy,progress,selected=visuallyselected",
        ".tab-icon-pending": "fadein,pinned,busy,progress,selected=visuallyselected,pendingicon",
        ".tab-icon-image": "src=image,triggeringprincipal=iconloadingprincipal,requestcontextid,fadein,pinned,selected=visuallyselected,busy,crashed,sharing,pictureinpicture",
        ".tab-sharing-icon-overlay": "sharing,selected=visuallyselected,pinned",
        ".tab-icon-overlay": "sharing,pictureinpicture,crashed,busy,soundplaying,soundplaying-scheduledremoval,pinned,muted,blocked,selected=visuallyselected,activemedia-blocked",
        ".tab-label-container": "pinned,selected=visuallyselected,labeldirection",
        ".tab-label-container.proton": "pinned,selected=visuallyselected,labeldirection",
        ".tab-label": "text=label,accesskey,fadein,pinned,selected=visuallyselected,attention",
        ".tab-label-container.proton .tab-label": "text=label,accesskey,fadein,pinned,selected=visuallyselected,attention",
        ".tab-icon-sound": "soundplaying,soundplaying-scheduledremoval,pinned,muted,blocked,selected=visuallyselected,activemedia-blocked,pictureinpicture",
        ".tab-label-container.proton .tab-secondary-label": "soundplaying,soundplaying-scheduledremoval,pinned,muted,blocked,selected=visuallyselected,activemedia-blocked,pictureinpicture",
        ".tab-close-button": "fadein,pinned,selected=visuallyselected",
      };
    }

    connectedCallback() {
      this.initialize();
    }

    initialize() {
      if (this._initialized) {
        return;
      }

      this.textContent = "";
      this.appendChild(this.constructor.fragment);
      this.initializeAttributeInheritance();
      this._initialized = true;
    }

    get container() {
		throw 4;
    }

    set _visuallySelected(val) { this.tab._visuallySelected = val; }
    set _selected(val) { this.tab._selected = val; }
    get pinned() { return this.tab.pinned; }
    get hidden() { return this.tab.hidden; }
    get muted() { return this.tab.muted; }
    get multiselected() { return this.tab.multiselected; }
    get beforeMultiselected() { return this.tab.beforeMultiselected; }
    get userContextId() { return this.tab.userContextId; }
    get soundPlaying() { return this.tab.soundPlaying; }
    get pictureinpicture() { return this.tab.pictureinpicture; }
    get activeMediaBlocked() { return this.tab.activeMediaBlocked; }
    get isEmpty() { return this.tab.isEmpty; }

    get soundPlayingIcon() { return this.querySelector(".tab-icon-sound"); }
    get overlayIcon() { return this.querySelector(".tab-icon-overlay"); }
    get throbber() { return this.querySelector(".tab-throbber"); }
    get iconImage() { return this.querySelector(".tab-icon-image"); }
    get sharingIcon() { return this.querySelector(".tab-sharing-icon-overlay"); }
    get textLabel() { return this.querySelector(".tab-label"); }
    get closeButton() { return this.querySelector(".tab-close-button"); }
  }

  customElements.define("vertical-tab", VTab, {
    extends: "tab",
  });
}

