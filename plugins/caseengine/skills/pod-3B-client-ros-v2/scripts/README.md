# Scripts - pod-3B-client-ros-v2

## build-client-ros-v2-docx.py

The populate-side mirror of `pod-3A-ros-template-v2/scripts/build-ros-template-v2-docx.py` - same primitives, same locked v2 shape. Reads `client-ros-v2-data.json`, emits the CE-branded `.docx` and the paired `.md` in one pass.

Differences from the template renderer, all deliberate:
- NO appendix (the Source Question Bank is internal to the template)
- Cover adds the firm name (under the episode title) and the recording date (under Prepared by Case Engine, omitted while TBD)
- Populate gates run before any render work: zero leftover {{...}} tokens, statics equal the template constants with tokens resolved (TEMPLATE_STATICS mirrors 3A-v2 statics.json v2.0.0), appendix absent from the payload, guest-framing zero, em-dash zero - plus the inherited AT-1/AT-2, ten-per-location, and 2-4-bullet gates.

Usage:
  python3 build-client-ros-v2-docx.py --data client-ros-v2-data.json \
      --output "E{N}: {Episode Title} // {Firm} // Client ROS v2 - {Location}.docx"

The DOCX uploads as `application/vnd.google-apps.document` (Drive auto-converts); the `.md` as `text/markdown`. NEVER upload the .md with convert=true.

If 3A-v2's statics or document shape change, update TEMPLATE_STATICS and the render order here in the same session - the two renderers must stay mirrors.
