# 同期チェック用pfsx ファイル作成
# 指定ファイル(xxx.aaa) の拡張子を取り、xxx.pfsx を生成する

# usage python gen_pfsx.py <file> <file> ...

import sys
from pathlib import Path

def main(template_base):
    for infile in sys.argv[1:]:
        inpath = Path(infile)
        stem = inpath.stem
        template = template_base.replace('__BASENAME__', stem)

        outfile = stem + '.pfsx'
        with open(outfile, 'w') as fo:
            fo.write(template)

template = """\
<?xml version="1.0" encoding="UTF-8"?>
<preferences version="1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/Prefs_v1.1.xsd">
    <pref key="FrameSize">
        <Object class="java.awt.Dimension">1580,900</Object>
    </pref>
    <pref key="LayoutManager.SelectedTabIndex">
        <Int>7</Int>
    </pref>
    <pref key="LayoutManager.VisibleMultiTierViewer">
        <String>mpi.eudico.client.annotator.viewer.TimeLineViewer</String>
    </pref>
    <pref key="MultiTierViewer.ActiveTierName">
        <String>テレノイド対話</String>
    </pref>
    <pref key="SelectionEndTime">
        <Long>0</Long>
    </pref>
    <pref key="LayoutManager.CurrentMode">
        <Int>1</Int>
    </pref>
    <prefGroup key="CommentViewer.Columns">
        <pref key="Sender">
            <Int>0</Int>
        </pref>
        <pref key="Comment">
            <Int>75</Int>
        </pref>
        <pref key="Creation Date">
            <Int>75</Int>
        </pref>
        <pref key="Tier">
            <Int>75</Int>
        </pref>
        <pref key="Modification Date">
            <Int>75</Int>
        </pref>
        <pref key="Recipient">
            <Int>0</Int>
        </pref>
        <pref key="Start Time">
            <Int>75</Int>
        </pref>
        <pref key="Initials">
            <Int>75</Int>
        </pref>
        <pref key="End Time">
            <Int>75</Int>
        </pref>
        <pref key="Thread">
            <Int>75</Int>
        </pref>
    </prefGroup>
    <prefList key="CommentViewer.Columns.Order">
        <String>Start Time</String>
        <String>End Time</String>
        <String>Tier</String>
        <String>Initials</String>
        <String>Comment</String>
        <String>Thread</String>
        <String>Sender</String>
        <String>Recipient</String>
        <String>Creation Date</String>
        <String>Modification Date</String>
    </prefList>
    <pref key="ActiveRecognizerName">
        <String>AAM-LR Phone level audio segmentation</String>
    </pref>
    <pref key="FrameLocation">
        <Object class="java.awt.Point">1055,63</Object>
    </pref>
    <pref key="SelectionBeginTime">
        <Long>0</Long>
    </pref>
    <prefGroup key="AAM-LR Phone level audio segmentation">
        <pref key="base_url">
            <String>http://lux17.mpi.nl/aamlr/</String>
        </pref>
        <pref key="source_audio">
            <String>__BASENAME__.wav</String>
        </pref>
    </prefGroup>
    <pref key="TimeScaleBeginTime">
        <Long>0</Long>
    </pref>
    <pref key="MediaTime">
        <Long>66</Long>
    </pref>
    <prefGroup key="TierColors">
        <pref key="テレノイド対話">
            <Object class="java.awt.Color">160,90,0</Object>
        </pref>
        <pref key="発話">
            <Object class="java.awt.Color">90,160,160</Object>
        </pref>
    </prefGroup>
    <prefList key="MultiTierViewer.TierOrder">
        <String>テレノイド対話</String>
        <String>発話</String>
    </prefList>
    <prefGroup key="IndividualPlayerVolumes">
        <pref key="__BASENAME__.MP4">
            <Float>0.5</Float>
        </pref>
        <pref key="__BASENAME__.wav">
            <Float>1.0</Float>
        </pref>
    </prefGroup>
    <pref key="LayoutManager.SplitPaneDividerLocation">
        <Int>236</Int>
    </pref>
    <prefList key="CommentViewer.Columns.Hidden">
        <String>Sender</String>
        <String>Recipient</String>
    </prefList>
</preferences>
"""

main(template)
