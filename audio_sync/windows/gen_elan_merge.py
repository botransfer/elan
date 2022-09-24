import sys
import os
import glob
import pympi.Elan

args = sys.argv
args.pop(0)

files = []
for f in args:
    files.extend(glob.glob(f))
    print(files)

for path in files:
    path = os.path.abspath(path)
    targetdir, filename = os.path.split(path)
    basename = os.path.splitext(filename)[0]
    print("processing merger", basename)

    path_elan = os.path.join(targetdir, basename + ".eaf")
    path_elan_sync = os.path.join(targetdir, basename + "_sync.eaf")
    sync_eaf = pympi.Elan.Eaf(path_elan_sync) 
    d_mp4 = int(sync_eaf.media_descriptors[0]["TIME_ORIGIN"])
    d_wav = int(sync_eaf.media_descriptors[1]["TIME_ORIGIN"])

    # if there is annotation .eaf file
    if os.path.exists(path_elan):
        anno_eaf = pympi.Elan.Eaf(path_elan)
        if d_wav!=0:
            for anno_ts, anno_time in anno_eaf.timeslots.items():
                anno_eaf.timeslots[anno_ts] = anno_time - d_wav

                # miss sync
                if anno_eaf.timeslots[anno_ts] < 0:
                    miss_file_name = path_elan
                    f = open("sync_miss_files.txt", "a", encoding='utf-8')
                    f.write(miss_file_name + "\n")
                    f.close()
                    break

            else:
                for anno_tier_name in anno_eaf.tiers.keys():
                    anno_eaf.copy_tier(sync_eaf,anno_tier_name)

        elif d_wav==0:
            # doubt sync
            if d_mp4 > 20000:
                    miss_file_name = path_elan
                    f = open("sync_doubt_files.txt", "a", encoding='utf-8')
                    f.write(miss_file_name + "\n")
                    f.close()

            for anno_tier_name in anno_eaf.tiers.keys():
                anno_eaf.copy_tier(sync_eaf,anno_tier_name)

        os.remove(path_elan)
        os.remove(path_elan_sync)
        pympi.Elan.to_eaf(path_elan, sync_eaf)

    # if there is not annotation .eaf file
    else:
        msg = "Error: annotation ELAN file exists: %s"
        raise SystemExit(msg % (path_elan))
