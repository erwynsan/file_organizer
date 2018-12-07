from filecmp import dircmp
import os, shutil



def print_diff_files(dcmp):
     print "========comparing: left: %s == right: %s ======" % (dcmp.left, dcmp.right)

#     for name in dcmp.diff_files:
#         print "diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right)
     for name in dcmp.left_only:
         #print "diff_file %s found in left only %s" % (name, dcmp.left)
         src_filename = dcmp.left + "/" + name
         dest_dir =  dcmp.right + "/" + name
         print "copying file %s to %s" % (src_filename, dest_dir)
         if os.path.isdir(src_filename) and not os.path.exists(dest_dir):
             shutil.copytree(src_filename, dest_dir)
         else:
             shutil.copy2(src_filename, dest_dir)

#     for name in dcmp.right_only:
#         print "diff_file %s found in right only %s" % (name, dcmp.right)

     for sub_dcmp in dcmp.subdirs.values():
         print_diff_files(sub_dcmp)

dcmp = dircmp('<left>', '<right>')
print_diff_files(dcmp)
