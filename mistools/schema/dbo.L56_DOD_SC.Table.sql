DROP TABLE [dbo].[L56_DOD_SC]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SC]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_SC](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SC01] [varchar](1) NULL,
	[SC02] [varchar](1) NULL,
	[SC03] [varchar](1) NULL,
	[SC04] [varchar](1) NULL,
	[SC05] [varchar](5) NULL,
	[SC06] [int] NULL,
	[SC07] [int] NULL,
	[SC08] [int] NULL,
	[SC09] [int] NULL,
	[SC10] [varchar](1) NULL,
	[SC11] [varchar](6) NULL,
	[SC18] [varchar](1) NULL,
 CONSTRAINT [PK_DOD_SC_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
